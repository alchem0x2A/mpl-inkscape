"""
A minimal backend to export TeX math into Inkscape svg files based on patching 
the original svg backend of matplotlib.
The backend used algorithm in original svg backend to determine the position, 
and writes raw math string to svg.
"""
import io
from matplotlib._pylab_helpers import Gcf
from matplotlib.backends.backend_mixed import MixedModeRenderer
from matplotlib.backend_bases import (
    _Backend, FigureCanvasBase, FigureManagerBase,
    GraphicsContextBase, RendererBase)
from matplotlib.figure import Figure
from matplotlib import cbook, __version__, rcParams

from matplotlib.backends.backend_svg import RendererSVG, FigureCanvasSVG


def replace_texcmd(s):
    """Replace the \\mathdefault commands in mtext string"""
    s = s.replace(r"\mathdefault", "")
    return s


class RendererInkSVG(RendererSVG):
    """
    Inherited from original svg backend. Even if mathmode is true,
     it renders the output as if in plain text mode, with proper  alignment.
    Only function to change from the parent class is the draw_text function
    """

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        clipid = self._get_clip(gc)
        print("use tex")
        if clipid is not None:
            self.writer.start(
                'g', attrib={'clip-path': 'url(#%s)' % clipid})

        if gc.get_url() is not None:
            self.writer.start('a', {'xlink:href': gc.get_url()})

        if rcParams['svg.fonttype'] == 'path':
            self._draw_text_as_path(gc, x, y, s, prop, angle, ismath, mtext)
        else:
            # When output using none, ismath is always False
            # TODO: better layout when drawing text
            s = replace_texcmd(s)
            self._draw_text_as_text(gc, x, y, s, prop, angle, False, mtext)

        if gc.get_url() is not None:
            self.writer.end('a')

        if clipid is not None:
            self.writer.end('g')


########################################################################
#
# The following functions and classes are for pyplot and implement
# window/figure managers, etc...
#
########################################################################


class FigureCanvasInkSVG(FigureCanvasSVG):
    """
    Inherited from FigureCanvasSVG and only need to call the RendererInkSVG class
    """

    def _print_svg(
            self, filename, fh, *, dpi=72, bbox_inches_restore=None, **kwargs):
        self.figure.set_dpi(72.0)
        width, height = self.figure.get_size_inches()
        w, h = width * 72, height * 72

        renderer = MixedModeRenderer(
            self.figure, width, height, dpi,
            RendererInkSVG(w, h, fh, filename, dpi),
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)
        renderer.finalize()


class FigureManagerInkSVG(FigureManagerBase):
    """
    Helper class for pyplot mode, wraps everything up into a neat bundle.

    For non-interactive backends, the base class is sufficient.

    Need to rewrite the renderer method
    """
    pass


########################################################################
#
# Now just provide the standard names that backend.__init__ is expecting
#
########################################################################

@_Backend.export
class _BackendSvgTeX(_Backend):
    FigureCanvas = FigureCanvasInkSVG
    FigureManager = FigureManagerInkSVG
