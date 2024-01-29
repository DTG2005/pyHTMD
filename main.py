import argparse
from lib.convs import conv_to_html, conv_to_md

#TODO: Directory usage as well
parser = argparse.ArgumentParser(description="Converts given MD file to HTML file or vice-versa.")

#Accepting arguments from CLI Parser
parser.add_argument("name", help="Accepts the name of the file or folder. Is required.", type=str)

#Extracting the argument from the parser
args = parser.parse_args()
name = args.name

#Error handling
if ".md" not in name and ".html" not in name:
    parser.error("Invalid name detected. Only filenames are allowed.")
else:
    if ".md" in name:
        with open(name, 'r') as f:
            text = []
            for i in f:
                text.append(i.rstrip('\n'))
            with open(name[:-3]+".html", "w") as g:
                g.write(conv_to_html(text))
    else:
        with open(name, 'r') as f:
            text = []
            for i in f:
                text.append(i.rstrip('\n'))
            with open(name[:-5]+".md", "w") as g:
                g.write(conv_to_md(text))