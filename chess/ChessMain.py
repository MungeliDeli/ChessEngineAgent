'''
class for handling user input and rendering the gamestate on the booard
'''
import pygame as p
from chess import  ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



# Initialize a global dictionary or images

def loadImages():
    pieces = [ 'wP' , 'wR' , 'wN' , 'wB' , 'wK' , 'wQ' ,'bP' ,'bR', 'bN' , 'bB' , 'bK' , 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png") , (SQ_SIZE , SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH , HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row , col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row , col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1] , gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen , gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen , gs):
    drawBoard(screen)
    drawPieces(screen , gs.board)




def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE , SQ_SIZE))



def drawPieces(screen , board):
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":  #if square is not empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE , SQ_SIZE))



if __name__ == "__main__":
    main()

