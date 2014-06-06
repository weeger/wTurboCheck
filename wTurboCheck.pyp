import c4d
import os

# wTurboCheck - Additionnal validation for
# turbosquid models submission. For deeper checks
# download Checkmate plugin from the Turbosquid website.
# This plugin is based on the CheckMate Pro Specification
# Available at http://support.turbosquid.com/entries/20203606-CheckMate-Pro-Specification

# Romain Weeger - www.wexample.com
# If you enjoy this plugin, please
# contact me, and say me hello \o/

PLUGIN_ID = 1032263
VERSION = '1.0'

# Command laucher from plugins menu
class wTurboCheckCommand(c4d.plugins.CommandData):
    dialog = None
    
    def Execute(self, doc):
        print 'wTurboCheck v' + VERSION + ' [c] Romain Weeger - www.wexample.com'
        #Get the selected objects, in the order in which they were selected
        object = doc.GetActiveObject()
        check_object(object, doc)
        return True

# Check if object match with Turbosquid rules
def check_object(object, doc):
    # This is a polygon object
    if isinstance(object, c4d.PolygonObject):
        message_error = ''
        message_success = ''
        # Create a new selection
        polygons_selection = object.GetPolygonS()
        polygons_selection.DeselectAll()
        
        # Check poles with 6 more "edge" (use polygons count)
        check_pole_limit = pole_limit(object, polygons_selection)
        if check_pole_limit!=0 :
            message_error += error_format('Found ' + str(check_pole_limit) + ' poles with more than 5 polygons (marked by polygon selection)', '2.2.3.2 No poles with more than 5 edges on the model')
        else :
             message_success += 'No poles with more than 5 polygons' + "\n"
        
        # Check object layer
        if layer_exists(object, doc)==False:
            message_error += error_format('Missing layer for ' + object.GetName(), '2.6.5 Objects are contained in a layer structure, with the layer having the same name as the product.')
        else :
            message_success += 'Object has layer : ' + object.GetLayerObject(doc) + "\n"
         
        c4d.EventAdd()
             
        # Display result.
        if message_error!='' :
            c4d.gui.MessageDialog(message_error)
        else :
            c4d.gui.MessageDialog(message_success)
            
    else :
        c4d.gui.MessageDialog('Please, select a polygon object...')
        
    return True

# Formated error messages
def error_format(message,rule) :
    return '- ' + message + ' : ' + rule + '\n\n'

# Define if object have a layer. We may add some validation
# if we sucess to retrive the final object name into the c4d scene.
def layer_exists(object, doc) :
    layer = object.GetLayerObject(doc)
    if layer!=None :
        return True
    else :
        return False

# Search for poles with more than 5 edges, and select it.
def pole_limit(object, polygons_selection):
    #Get polygons list
    polygons = object.GetAllPolygons()
    point_count = object.GetPointCount()
    # Prepare neighbor object.
    neighbor = c4d.utils.Neighbor()
    neighbor.Init(object)
    # Create a counter of 
    poles_exceed = 0
    for point_id in xrange(point_count):
        point_polygons = neighbor.GetPointPolys(point_id) 
        if len(point_polygons) > 5 :
            for polygon_index in point_polygons :
                polygon = object.GetPolygon(polygon_index)
                polygons_selection.Select(polygon_index)
            poles_exceed = poles_exceed + 1
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