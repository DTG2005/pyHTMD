def getStringSlices(text: str, bracketType : str = "*") -> list[int, list[str]]:
    indexBeg = text.find(bracketType)
    indexEnd = text.find(bracketType, indexBeg+1)

    return [indexEnd+len(bracketType), [text[:indexBeg], text[indexBeg+len(bracketType):indexEnd], text[indexEnd+len(bracketType):]]]

def getBracketStringSlices(text: str, bracketType : str = "[]"):
    indexBeg = text.find(bracketType[0])
    indexEnd = text.find(bracketType[1])

    return [indexEnd + 1, [text[:indexBeg], text[indexBeg+1:indexEnd], text[indexEnd+1:]]]