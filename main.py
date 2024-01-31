import markdown
import markdownify
import argparse
import os

parser = argparse.ArgumentParser(description="Converts HTML file into MD and outputs it into the same filename but in different format. Recurses through a directory incase a directory path is provided.")

made = False
parser.add_argument("name", help="Name of the file or directory to be used.")
parser.add_argument("--complete",action="store_true", help="If file is md, makes the conversion a browser ready html file.")

args = parser.parse_args()
name = args.name 

html_def = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>\n"""


if ".html" in name:
    with open(name, 'r') as f:
        text = f.read()
        with open(name.replace(".html", ".md"), 'w') as g:
            g.write(markdownify.markdownify(text))
elif ".md" in name:
    with open(name, 'r') as f:
        text = f.read()
        with open(name.replace(".md", ".html"), 'w') as g:
            if args.complete:
                g.write(html_def+markdown.markdown(text)+"\n</body></html>")
            else:
                g.write(markdown.markdown(text))

elif os.path.isdir(name):
    for file in os.listdir(name):
        pathx = name+"\\conv"
        if os.path.isdir(pathx) and not made:
            pathx+="_new"
        try:
            os.mkdir(pathx)
        except:
            pass
        made=True

        if ".html" in file:
            with open(name+"\\"+file, 'r') as f:
                text = f.read()
                with open(pathx + "\\"+file.replace(".html", ".md"), 'w') as g:
                    g.write(markdownify.markdownify(text))
        elif ".md" in file:
            with open(name+"\\"+file, 'r') as f:
                text = f.read()
                with open(pathx + "\\"+file.replace(".md", ".html"), 'w') as g:
                    g.write(markdown.markdown(text))
else:
    parser.error("The name must be the name of a file.")
