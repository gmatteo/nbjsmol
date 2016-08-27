_jmolapp_nums = []

def display_structure(structure):
    global _jmolapp_nums
    if not _jmolapp_nums:
        _jmolapp_nums.append(1)
    else:
        _jmolapp_nums.append(_jmolapp_nums[-1] + 1)

    # Get the structure and write tempoary cif file.
    structure = Structure.as_structure(structure)
    import os, tempfile
    datadir = os.path.join(os.getcwd(), "ipynb_jsmoldata")
    if not os.path.exists(datadir): os.mkdir(datadir)
    #datadir = os.getcwd()
    _, cif_file = tempfile.mkstemp(suffix='.cif', dir=datadir, text=True)
    structure.to(fmt="cif", filename=cif_file)

    # Dictionary used in template string.
    opts = dict(
        cif_file=os.path.relpath(cif_file),
        jmolapp_id="jmolapp_id%d" % _jmolapp_nums[-1],
    )
    #print(opts)

    #<script type="text/javascript" src="//file/local/jmol/jsmol/JSmol.min.js"></script>
    #<script type="text/javascript" src="//file/Users/gmatteo//local/jmol/jsmol/JSmol.min.js"></script>
    #<script type="text/javascript" src="JSmol.min.js"></script>
    #//<script type="text/javascript" src="jquery/jquery.min.js"></script>
    #//<script type="text/javascript" src="JSmol.lite.nojq.js"></script>
    #//<script type="text/javascript" src="jsmol/JSmol.min.nojq.js"></script>
    #//<script type="text/javascript" src="JSmol.min.nojq.js"></script>
    javascript = """
<script type="text/javascript" src="jquery/jquery.min.js"></script>
<script type="text/javascript" src="nbjsmol/jsmol/JSmol.min.nojq.js"></script>

<script type="text/javascript">
//$(window).ready(function() {
$("#%(jmolapp_id)s").ready(function() {

    Info = {
        antialiasDisplay: true,
        //disableJ2SLoadMonitor: true,
        width: 500,
        height: 500,
        color: "black",
        //addSelectionOptions: true,
        serverURL: "mbjsmol/jsmol/php/jsmol.php",
        script: "load %(cif_file)s;",
        //src: "%(cif_file)s",
        use: "HTML5",
        j2sPath: "jsmol/j2s",          // only used in the HTML5 modality
        //readyFunction: null,
        //defaultModel: ":dopamine", // PubChem -- use $ for NCI
        bondWidth: 4,
        zoomScaling: 1.5,
        pinchScaling: 2.0,
        mouseDragFactor: 0.5,
        touchDragFactor: 0.15,
        multipleBondSpacing: 4,
        //spin: true,
        //spinRateX: 0.2,
        //spinRateY: 0.5,
        //spinFPS: 20,
        //disableInitialConsole: true,
        debug: false
    },

  //Jmol._document = null;
  $("#%(jmolapp_id)s").html(Jmol.getAppletHtml("%(jmolapp_id)s", Info));
  //$("#%(jmolapp_id)s").html(Jmol.getApplet("%(jmolapp_id)s", Info));
});

</script>
""" % opts

    html_code = '<div id="%s"></div>' % opts["jmolapp_id"]

    print(javascript + html_code)
    from IPython.display import HTML, display
    return display(HTML(javascript + html_code))
