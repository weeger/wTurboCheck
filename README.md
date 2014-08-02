wTurboCheck
===========

wTurboCheck provides additional validation for TurboSquid models submission on polygons objects on Cinema4D R15. For deeper checks download Checkmate plugin from the Turbosquid website. This plugin is based on the CheckMate Pro Specification. Only two more check are provided now on polygons model objects :

- Check for poles containing more than 5 edges by points
- Check if object is contained into a layer
- Return polygon count (not subdivided), and symmetry total estimation
- Return points count (not subdivided), and symmetry total estimation, taking care of merged points

To run it, just install it as a standard C4D plugin, select your mesh add launch it from the plugins menu. It should return the result of his inspection.
