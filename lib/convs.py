from .dep import getBracketStringSlices, getStringSlices

def conv_to_html(lines : list[str]) -> str:
    html_text = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
"""
    isInOList = [False,1]
    isInUList = [False,1]
    for line in lines:
        if line:
            #handling blockquotes
            if line[0] == ">":
                html_text+= ("<blockquote>" +line[2:]+"</blockquote>")
                continue

            #Handling indents
            elif line[0] == " ":
                count2 = 1
                while True:
                    if line[count2*4] != " ":
                        break
                    else:
                        count+=1
                if isInOList[0] and isInOList[1]<count2:
                    html_text += "\t<ol>\n"
                    isInOList[1] +=1
                    html_text += ("\t<li>\n" + line[count2*4:] + "</li>")
                elif isInUList[0] and isInUList[1]<count2:
                    html_text += "\t<ul>\n"
                    isInUList[1] +=1
                    html_text += ("\t<li>\n" + line[count2*4:] + "</li>")
                elif isInOList[1] == count2 or isInUList[1] == count2:
                    html_text += ("\t<li>\n" + line[count2*4:] + "</li>")
                elif count2 == 2:
                    html_text+= ("<code>" + line[count2*4] + "<code>")

            #Terminating Ordered lists if they are no longer continuing
            elif isInOList[0] and not (line[0].isdigit and line[1] == "."):
                html_text += "</ol>\n"
                isInOList[0] = False

            #Same with Unordered lists
            elif isInUList[0] and not (line[0] == "-"):
                html_text += "</ul>\n"
                isInUList[0] = False

            #Handling Headings
            elif line[0] == "#":
                count = 1
                while True:
                    if line[count] == "#":
                        count+=1
                    else:
                        line = line[count+1:]
                        break
                html_text+= ("<h"+str(count)+">")
                html_text+=line
                html_text+=("</h"+str(count)+">\n")
                continue
            
            #Handling Ordered lists
            elif line[0].isdigit and line[1] == ".":
                if not isInOList[0]:
                    html_text += "<ol>\n"
                    html_text += ("<li>"+line[3:]+"</li>\n")
                    isInOList[0] = True
                else:
                    if isInOList[1] != 1:
                        html_text += ("</ol>\n")
                    html_text += ("<li>"+ line[3:] + "</li>\n")   
                continue

            #Handling Unordered lists
            elif line[0] == "-":
                if not isInUList[0]:
                    html_text += "<ul>\n"
                    html_text += ("<li>"+line[2:]+"</li>\n")
                    isInUList[0] = True
                else:
                    if isInOList[1] != 1:
                        html_text += ("</ol>\n")
                    html_text += ("<li>"+ line[2:] + "</li>\n")
                continue
    
            #Handling images
            elif line[0] == "!":
                x = line.find("]")
                alt = line[2:x]
                y = line.find(")")
                src = line[x+2:y]
                if src[0] == "/":
                    src = src[1:]
                html_text += ("<img alt = " + alt + " src = " + src+ ">\n")
                continue
                
            #Handling paragraph markdown
            else:
                html_text += "<p>"
                chrCnt = 0
                while chrCnt<=len(line)-1:
                    a = line[chrCnt]

                    #This checks strong and emphasised markdown
                    if a=="*":
                        if line[chrCnt+1] == "*":
                            if line[chrCnt+2] == "*":
                                strList = getStringSlices(line[chrCnt:], "***")
                                html_text += ("<strong><em>" + strList[1][1] + "</em></strong>")
                                chrCnt = strList[0]
                                print("both")
                                continue
                            strList = getStringSlices(line[chrCnt:], "**")
                            html_text += ("<strong>" + strList[1][1] + "</strong>")
                            chrCnt += strList[0]
                            print(chrCnt)
                            continue
                        strList = getStringSlices(line[chrCnt:])
                        html_text += ("<em>" + strList[1][1] + "</em>")
                        chrCnt = strList[0]
                        print('em')
                        continue
                    elif a=="_":
                        if line[chrCnt+1] == "_":
                            if line[chrCnt+2] == "_":
                                strList = getStringSlices(line[chrCnt:], "___")
                                html_text += ("<strong><em>" + strList[1][1] + "</em></strong>")
                                chrCnt += strList[0]
                                continue
                            strList = getStringSlices(line[chrCnt:], "__")
                            html_text += ("<strong>" + strList[1][1] + "</strong>")
                            chrCnt += strList[0]
                            print(chrCnt)
                            continue
                        strList = getStringSlices(line[chrCnt:], "_")
                        html_text += ("<em>" + strList[1][1] + "</em>")
                        chrCnt += strList[0]
                        print('em')
                        continue

                    #This checks inline code markdown
                    elif a == "`":
                        if line[chrCnt+1] == '`':
                            strList = getStringSlices(line[chrCnt:], "``")
                            html_text += ("<code>" + strList[1][1] + "</code>")
                            chrCnt += strList[0]
                            continue
                        strList = getStringSlices(line[chrCnt:], "`")
                        html_text += ("<code>" + strList[1][1] + "</code>")
                        chrCnt += strList[0]
                        continue

                    #And this checks hyperlink markdown
                    elif a == "[":
                        strList = getBracketStringSlices(line[chrCnt:])
                        strNext = strList[1][2]
                        strNextList = getBracketStringSlices(strNext, "()")
                        src = strNextList[1][1]
                        chrCnt += strNextList[0] + strList[0]
                        html_text += ("<a href = \"" + src + "\">" + strList[1][1] + "</a>")
                        continue
                    html_text += a
                    chrCnt +=1
                html_text += "</p>\n"

        elif isInUList[0]:
            html_text += "</ul>\n"
            isInUList[0] = False
        elif isInOList[0]:
            html_text += "</ol>\n"
            isInOList[0] = False

    if isInUList[0]:
        html_text += "</ul>\n"
    elif isInOList[0]:
        html_text += "</ol>\n"
    html_text += "</body>"
    return html_text

def conv_to_md(lines : list[str]) -> str:
    mdText = ""
    isInOList = False
    isInUList = False
    index = 0

    #Finding Body Tag and then proceeding from there
    for line in lines:
        if "<body>" in line:
            index = lines.index(line)
    lines = lines[index+1:len(lines)-2]

    #Now starting to proceed
    for line in lines:
        line =line.strip()

        #Handling Paragraph Markdown
        if line[:3] == "<p>":
            line = "".join(line.rsplit('/', 1))
            strList = getStringSlices(line, "<p>")
            mdText += f"{strList[1][1]}\n"
            continue
    
    return mdText