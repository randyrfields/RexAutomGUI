def drawTOF(self, index, values):
    offset = 10
    self.rect = {}
    self.oval = {}
    self.cellwidth = 10
    self.cellheight = 10
    for column in range(4):
        for row in range(4):
            colr = values[(column * 4) + (row)]
            x1 = column * self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            x1 += offset
            x2 += offset
            y1 += offset
            y2 += offset
            # if index == 4:
            #     color = "#90EE90"
            # else:
            #     color = "white"
            color = "white"

            self.rect[row, column] = self.canvases[index].create_rectangle(
                x1, y1, x2, y2, fill=color, tags="rect"
            )
            fillcolor = "white"
            self.oval[row, column] = self.canvases[index].create_oval(
                x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill=fillcolor, tags="oval"
            )
