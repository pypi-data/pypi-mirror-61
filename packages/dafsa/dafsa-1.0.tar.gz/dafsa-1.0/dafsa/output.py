"""
Module holding output functions.

Please note that this module is excluded from automatic security analysis,
as it must perform system calls using `subprocess`.
"""

# Python standard imports
import pathlib
import subprocess
import tempfile


def graphviz_output(dot_source, output_file, dpi=300):
    """
    Generates a visualization by calling the local `graphviz`.

    The filetype will be decided from the extension of the `filename`.

    Parameters
    ----------
    output_file : str
        The path to the output file.
    dpi : int
        The output resolution. Defaults to 300.

    Returns
    -------
    ret : subprocess.CompletedProcess
        A `CompleteProcess` instance, as returned by the `subprocess` call.
    """

    # Write to a named temporary file so we can call `graphviz`
    handler = tempfile.NamedTemporaryFile()
    handler.write(dot_source)
    handler.flush()

    # Get the filetype from the extension and call graphviz
    suffix = pathlib.PurePosixPath(output_file).suffix
    ret = subprocess.run(
        [
            "dot",
            "-T%s" % suffix[1:],
            "-Gdpi=%i" % dpi,
            "-o",
            output_file,
            handler.name,
        ],
        check=True,
        shell=False,
    )

    # Close the temporary file
    handler.close()

    return ret
