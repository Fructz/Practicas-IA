import java.util.Arrays;

public class Gato {

    private char[][] board;
    private static final int BOARD_SIZE = 4;
    private static final char PLAYER_X = 'X';
    private static final char PLAYER_O = 'O';
    private static final char EMPTY = '-';

    public Gato() {
        board = new char[BOARD_SIZE][BOARD_SIZE];
        for (int i = 0; i < BOARD_SIZE; i++) {
            Arrays.fill(board[i], EMPTY);
        }
    }

    public char[][] getBoard() {
        return board;
    }

    public void setBoard(char[][] board) {
        this.board = board;
    }

    public boolean isMoveValid(int row, int col) {
        return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE && board[row][col] == EMPTY;
    }

    public void makeMove(int row, int col, char player) {
        board[row][col] = player;
    }

    public boolean checkWinner(char player) {
        // Verificar filas
        for (int i = 0; i < BOARD_SIZE; i++) {
            if (board[i][0] == player && board[i][1] == player && board[i][2] == player && board[i][3] == player) {
                return true;
            }
        }

        // Verificar columnas
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (board[0][j] == player && board[1][j] == player && board[2][j] == player && board[3][j] == player) {
                return true;
            }
        }

        // Verificar diagonal principal
        if (board[0][0] == player && board[1][1] == player && board[2][2] == player && board[3][3] == player) {
            return true;
        }

        // Verificar diagonal secundaria
        if (board[0][3] == player && board[1][2] == player && board[2][1] == player && board[3][0] == player) {
            return true;
        }

        return false;
    }

    public boolean isBoardFull() {
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    public Move findBestMove(char player) {
        int bestScore = (player == PLAYER_X) ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        Move bestMove = new Move(-1, -1);

        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    board[i][j] = player;
                    int score = minimax(board, 0, false, Integer.MIN_VALUE, Integer.MAX_VALUE);
                    board[i][j] = EMPTY; // Deshacer el movimiento

                    if (player == PLAYER_X) {
                        if (score > bestScore) {
                            bestScore = score;
                            bestMove = new Move(i, j);
                        }
                    } else {
                        if (score < bestScore) {
                            bestScore = score;
                            bestMove = new Move(i, j);
                        }
                    }
                }
            }
        }
        return bestMove;
    }

    private int minimax(char[][] currentBoard, int depth, boolean isMaximizingPlayer, int alpha, int beta) {
        // Casos base
        if (checkWinner(PLAYER_X)) return 10;
        if (checkWinner(PLAYER_O)) return -10;
        if (isBoardFull()) return 0;

        if (isMaximizingPlayer) {
            int bestScore = Integer.MIN_VALUE;
            for (int i = 0; i < BOARD_SIZE; i++) {
                for (int j = 0; j < BOARD_SIZE; j++) {
                    if (currentBoard[i][j] == EMPTY) {
                        currentBoard[i][j] = PLAYER_X;
                        int score = minimax(currentBoard, depth + 1, false, alpha, beta);
                        currentBoard[i][j] = EMPTY;
                        bestScore = Math.max(bestScore, score);
                        alpha = Math.max(alpha, bestScore);
                        if (beta <= alpha) {
                            break; // Poda Beta
                        }
                    }
                }
            }
            return bestScore;
        } else {
            int bestScore = Integer.MAX_VALUE;
            for (int i = 0; i < BOARD_SIZE; i++) {
                for (int j = 0; j < BOARD_SIZE; j++) {
                    if (currentBoard[i][j] == EMPTY) {
                        currentBoard[i][j] = PLAYER_O;
                        int score = minimax(currentBoard, depth + 1, true, alpha, beta);
                        currentBoard[i][j] = EMPTY;
                        bestScore = Math.min(bestScore, score);
                        beta = Math.min(beta, bestScore);
                        if (beta <= alpha) {
                            break; // Poda Alpha
                        }
                    }
                }
            }
            return bestScore;
        }
    }
}