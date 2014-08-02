import c4d
import os

# TODO : Count points / polygons of a symetrysed object
# polygon = polygons * 2
# points = points * 2 - points_merged

# wTurboCheck

# Copyright Romain WEEGER 2010 / 2014
# http://www.wexample.com
# Licensed under the MIT and GPL licenses :
# - http://www.opensource.org/licenses/mit-license.php
# - http://www.gnu.org/licenses/gpl.html
# If you enjoy this plugin, please
# contact me, and say me hello \o/

# Additional validation for Turbosquid models submission. For deeper checks
# download Checkmate plugin from the Turbosquid website.
# This plugin is based on the CheckMate Pro Specification
# Available at http://support.turbosquid.com/entries/20203606-CheckMate-Pro-Specification

PLUGIN_ID = 1032263
VERSION = '1.2'
OBJECT_SYMMETRY_ID = 5142

# Command laucher from plugins menu
class wTurboCheckCommand(c4d.plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        print 'wTurboCheck v' + VERSION + ' [c] Romain Weeger - www.wexample.com'
        # Get the selected objects, in the order in which they were selected
        check_object(doc.GetActiveObject(), doc)
        return True


# Check if object match with Turbosquid rules
def check_object(object_check, doc):
    # This is a polygon object
    if isinstance(object_check, c4d.PolygonObject):
        message_error = ''
        message_success = ''
        # Create a new selection
        polygons_selection = object_check.GetPolygonS()
        polygons_selection.DeselectAll()

        # Check poles with 6 more "edge" (use polygons count)
        check_pole_limit = pole_limit(object_check, polygons_selection)
        if check_pole_limit != 0:
            message_error += error_format(
                'Found ' + str(check_pole_limit) + ' poles with more than 5 polygons (marked by polygon selection)',
                '2.2.3.2 No poles with more than 5 edges on the model')
        else:
            message_success += 'OK : No poles with more than 5 polygons' + "\n"

        # Check object layer
        if layer_exists(object_check, doc) is False:
            message_error += error_format('Missing layer for ' + object_check.GetName(),
                                          '2.6.5 Objects are contained in a layer structure, ' +
                                          'with the layer having the same name as the product.')
        else:
            message_success += 'OK : Object has layer : ' + object_check.GetLayerObject(doc).GetName() + "\n"

        c4d.EventAdd()

        # Check if symmetry object exists
        symmetric = False
        object_symmetry = {}
        object_symmetry_axis_index = 0
        object_parent = object_check
        while symmetric is False and object_parent:
            if isinstance(object_parent, c4d.BaseObject) and object_parent.CheckType(OBJECT_SYMMETRY_ID):
                symmetric = True
                object_symmetry = object_parent
                # Search to symmetry axis
                # XY => Z
                if object_symmetry[c4d.SYMMETRYOBJECT_PLANE] == 0:
                    object_symmetry_axis_index = 2
                # ZY => X
                elif object_symmetry[c4d.SYMMETRYOBJECT_PLANE] == 1:
                    object_symmetry_axis_index = 0
                # XZ => Y
                elif object_symmetry[c4d.SYMMETRYOBJECT_PLANE] == 2:
                    object_symmetry_axis_index = 1
            # Search upper
            object_parent = object_parent.GetUp()

        # Count polygons
        polygons_length = len(object_check.GetAllPolygons())
        message_success += '- ' + str(polygons_length) + ' polygons'
        if symmetric is True:
            message_success += ' (' + str(polygons_length * 2) + ' symmetrical)'
        message_success += "\n"

        # Count points
        points_length = len(object_check.GetAllPoints())
        message_success += '- ' + str(points_length) + ' points'

        if symmetric is True:
            points_length_sym = 0
            tolerance = object_symmetry[c4d.SYMMETRYOBJECT_TOLERANCE]
            # Search for merged points
            points = object_check.GetAllPoints()
            for point in points:
                # Use default symmetry rounding
                if not -tolerance <= point[object_symmetry_axis_index] <= tolerance:
                    points_length_sym += 1

            message_success += ' (' + str(points_length + points_length_sym) + \
                               ' symmetrical, or ' + str(points_length) + ' + ' + str(points_length_sym) + ')'
        message_success += "\n"

        # Display result.
        if message_error != '':
            c4d.gui.MessageDialog(message_error)
        else:
            c4d.gui.MessageDialog(message_success)

    else:
        c4d.gui.MessageDialog('Please, select a polygon object...')

    return True


# Formatted error messages
def error_format(message, rule):
    return 'KO : ' + message + ' : ' + rule + '\n\n'


# Define if object have a layer. We may add some validation
# if we success to retrieve the final object name into the c4d scene.
def layer_exists(object_check, doc):
    layer = object_check.GetLayerObject(doc)
    if layer is not None:
        return True
    else:
        return False


# Search for poles with more than 5 edges, and select it.
def pole_limit(object_check, polygons_selection):
    point_count = object_check.GetPointCount()
    # Prepare neighbor object.
    neighbor = c4d.utils.Neighbor()
    neighbor.Init(object_check)
    # Create a counter of 
    poles_exceed = 0
    for point_id in xrange(point_count):
        point_polygons = neighbor.GetPointPolys(point_id)
        if len(point_polygons) > 5:
            for polygon_index in point_polygons:
                polygons_selection.Select(polygon_index)
            poles_exceed += 1
    return poles_exceed


if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(dir, "res", "icon.tif"))
    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str="wTurboCheck",
        info=0,
        help="...",
        dat=wTurboCheckCommand(),
        icon=icon)