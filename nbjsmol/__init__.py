# coding: utf-8
from __future__ import division, unicode_literals, print_function, absolute_import

import os
import tempfile
import uuid

from shutil import copyfile

def _get_tmpfile(ext, text=True):
    """
    Return a temporary file with extension `ext`. The file is located inside the
    `ipynb_jsmoldata` directory created in the current working directory.
    This trick is needed due to the policy used by browsers to load local files.
    """
    datadir = os.path.join(os.getcwd(), "ipynb_jsmoldata")
    if not os.path.exists(datadir): os.mkdir(datadir)
    _, mypath = tempfile.mkstemp(suffix=ext, dir=datadir, text=text)
    return mypath


def _link_nbjsmol_dir():
    """
    Create a symbolic link in the cwd() pointing to the directory with the notebook extensions.
    This trick is needed due to the policy used by browsers to load local files.
    """
    from notebook.nbextensions import _nbextension_dirs
    for d in _nbextension_dirs():
        dirpath = os.path.join(d, "nbjsmol")
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            #print("Found nbjsmol notebook extension in drectory:", dirpath)
            if not os.path.exists("nbjsmol"):
                os.symlink(dirpath, "nbjsmol")
            return dirpath
    return None


def nbjsmol_display(data, ext=None, width=500, height=500, color="black",
                    spin="false", debug="false", text=True, html=False):
    """
    Display a structure in the jupyter notebook. `data` is either a file with geometrical
    information in one of the formats supported by jsmol (detected from the file extension) or a string.

    Args:
        data: Filename or string with geometrical information.

        ext:
        width:
        height:
        color:
        spin:
        debug:
        text:
        html:

    Returns:
        html string if `html` is set to True.
    """
    if ext is None:
        # Assume data is path
        root, ext = os.path.splitext(data)
        mypath = _get_tmpfile(ext, text=text)
        copyfile(data, mypath)
    else:
        # Assume data is string with structure.
        if ext is None:
            raise ValueError("ext must be provided when the structure is passed through a string.")
        mypath = _get_tmpfile(ext, text=text)
        with open(mypath, "w") as fh:
            fh.write(data)

    nbextdir = _link_nbjsmol_dir()
    if nbextdir is None:
        print("Cannot find nbjsmol directory to link")

    # Dictionary used in template string.
    opts = dict(
        jsmolapp_id="jsmolapp_id%d" % int(uuid.uuid4()),
        mypath=os.path.relpath(mypath),
        width=width,
        height=height,
        color=color,
        spin=spin,
        debug=debug,
    )
    #//<script type="text/javascript" src="jquery/jquery.min.js"></script>
    #//<script type="text/javascript" src="jsmol/JSmol.min.nojq.js"></script>

    html = """
<div id="%(jsmolapp_id)s" class=jsmolapp_div></div>

<script type="text/javascript" src="nbjsmol/jsmol/JSmol.min.js"></script>

<script type="text/javascript">
$("#%(jsmolapp_id)s").ready(function() {

    Info = {
        antialiasDisplay: true,
        //disableJ2SLoadMonitor: true,
        width: %(width)d,
        height: %(height)d,
        color: "%(color)s",
        //addSelectionOptions: true,
        serverURL: "nbjsmol/jsmol/php/jsmol.php",
        script: "load %(mypath)s;",
        //src: "%(mypath)s",
        use: "HTML5",
        j2sPath: "nbjsmol/jsmol/j2s",  // only used in the HTML5 modality
        //readyFunction: null,
        //bondWidth: 4,
        //pinchScaling: 2.0,
        //multipleBondSpacing: 4,
        spin: %(spin)s,
        disableInitialConsole: true,
        disableJ2SLoadMonitor: true,
        debug: %(debug)s
    },

  $("#%(jsmolapp_id)s").html(Jmol.getAppletHtml("%(jsmolapp_id)s", Info));
});
</script>

<style>
#%(jsmolapp_id)s {
    width: 50%%;
    margin: 0 auto;
}
</style>
""" % opts

    if debug == "true": print(html)
    if html: return html
    from IPython.display import HTML, display
    return display(HTML(html))


# Jupyter Extension points
#def _jupyter_nbextension_paths():
#    return [dict(
#        section="notebook",
#        # the path is relative to the `my_fancy_module` directory
#        src="static",
#        # directory in the `nbextension/` namespace
#        dest="my_fancy_module",
#        # _also_ in the `nbextension/` namespace
#        require="my_fancy_module/index")]
#
#def load_jupyter_server_extension(nbapp):
#    nbapp.log.info("my module enabled!")
