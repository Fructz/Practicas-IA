import java.util.Scanner;


public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Gato game = new Gato();

        System.out.println("¡Bienvenido al juego de Gato 4x4!");
        System.out.println("Tú eres 'X' y la máquina es 'O'.");
        printBoard(game.getBoard());

        while (true) {
            // Turno del jugador (humano)
            System.out.print("Ingresa tu jugada (fila y columna, de 0 a 3, separadas por un espacio): ");
            int playerRow = scanner.nextInt();
            int playerCol = scanner.nextInt();

            if (playerRow < 0 || playerRow >= 4 || playerCol < 0 || playerCol >= 4) {
                System.out.println("Movimiento inválido. Los valores deben estar entre 0 y 3. Inténtalo de nuevo.");
                continue;
            }

            if (game.isMoveValid(playerRow, playerCol)) {
                game.makeMove(playerRow, playerCol, 'X');
                printBoard(game.getBoard());

                if (game.checkWinner('X')) {
                    System.out.println("¡Felicidades! ¡Has ganado!");
                    break;
                }
                if (game.isBoardFull()) {
                    System.out.println("¡El juego ha terminado en empate!");
                    break;
                }

                // Turno de la máquina
                System.out.println("La máquina está pensando...");
                Move bestMove = game.findBestMove('O');
                game.makeMove(bestMove.row, bestMove.col, 'O');
                System.out.println("La máquina ha jugado en la fila " + bestMove.row + " y columna " + bestMove.col);
                printBoard(game.getBoard());

                if (game.checkWinner('O')) {
                    System.out.println("¡La máquina ha ganado! ¡Has perdido!");
                    break;
                }
                if (game.isBoardFull()) {
                    System.out.println("¡El juego ha terminado en empate!");
                    break;
                }
            } else {
                System.out.println("Movimiento inválido. La casilla ya está ocupada. Inténtalo de nuevo.");
            }
        }
        scanner.close();
    }

    private static void printBoard(char[][] board) {
        System.out.println("-------------");
        for (int i = 0; i < 4; i++) {
            System.out.print("| ");
            for (int j = 0; j < 4; j++) {
                System.out.print(board[i][j] + " | ");
            }
            System.out.println();
            System.out.println("-------------");
        }
    }
}
