import random
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from panic_screen import PANIC_TEXT, PANIC_TEXT_COLOR

LEVELS = {
    "beginner": {"rows": 9, "cols": 9, "mines": 10},
    "intermediate": {"rows": 12, "cols": 12, "mines": 20},
    "expert": {"rows": 14, "cols": 18, "mines": 35},
}

NUMBER_COLORS = {
    1: "#4fc1ff",
    2: "#4ec9b0",
    3: "#dcdcaa",
    4: "#c586c0",
    5: "#ce9178",
    6: "#f44747",
    7: "#d4d4d4",
    8: "#858585",
}

class Cell(QLabel):
    leftClicked = Signal(int, int)
    rightClicked = Signal(int, int)
    doubleClicked = Signal(int, int)

    def __init__(self, r, c):
        super().__init__(".")
        self.r = r
        self.c = c
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.count = 0
        self.setFixedSize(36, 36)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Courier New", 13, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.render_hidden()

    def render_hidden(self):
        self.setText(".")
        self.setStyleSheet(
            "background-color:#1c1c1c; color:#5a5a5a; border:1px solid #2d2d2d;"
        )

    def render_flagged(self):
        self.setText("F")
        self.setStyleSheet(
            "background-color:#1c1c1c; color:#ce9178; border:1px solid #2d2d2d;"
        )

    def render_mine(self):
        self.setText("X")
        self.setStyleSheet(
            "background-color:#2d1c1c; color:#f44747; border:1px solid #2d2d2d;"
        )

    def render_wrong_flag(self):
        self.setText("F")
        font = self.font()
        font.setStrikeOut(True)
        self.setFont(font)
        self.setStyleSheet(
            "background-color:#2d1c1c; color:#f44747; border:1px solid #f44747;"
        )

    def render_revealed(self):
        self.is_revealed = True
        if self.count > 0:
            self.setText(str(self.count))
            color = NUMBER_COLORS.get(self.count, "#d4d4d4")
            self.setStyleSheet(
                f"background-color:#252526; color:{color}; border:1px solid #333333;"
            )
        else:
            self.setText(" ")
            self.setStyleSheet(
                "background-color:#252526; color:#d4d4d4; border:1px solid #333333;"
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit(self.r, self.c)
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.r, self.c)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit(self.r, self.c)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Console Debugger")
        self.setStyleSheet("background-color:#1e1e1e; color:#d4d4d4;")

        self.current_level = "beginner"
        self.board = []
        self.cells = []
        self.game_over = False
        self.first_click = True
        self.is_panicked = False

        self._build_ui()
        self.init_board()

        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self.toggle_panic)


    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)

        self.header_label = QLabel()
        self.header_label.setStyleSheet("color:#6a9955; font-size:14px;")
        self.header_label.setFont(QFont("Courier New", 11))
        root.addWidget(self.header_label)

        controls = QHBoxLayout()
        self.level_buttons = {}
        for key, label in [
            ("beginner", "[SYS_LEV_1]"),
            ("intermediate", "[SYS_LEV_2]"),
            ("expert", "[SYS_LEV_3]"),
        ]:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, k=key: self.change_level(k))
            controls.addWidget(btn)
            self.level_buttons[key] = btn

        reset_btn = QPushButton("// RESET")
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.clicked.connect(self.init_board)
        controls.addWidget(reset_btn)
        controls.addStretch()
        root.addLayout(controls)
        self._style_buttons()

        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet(
            "background-color:#181818; border:1px solid #3c3c3c;"
        )
        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(12, 12, 12, 12)
        root.addWidget(self.grid_frame, alignment=Qt.AlignLeft)

        self.status_label = QLabel("> Status: System active.")
        self.status_label.setStyleSheet("color:#858585; font-size:13px;")
        self.status_label.setFont(QFont("Courier New", 10))
        root.addWidget(self.status_label)

        self.panic_label = QLabel(PANIC_TEXT)
        self.panic_label.setStyleSheet(f"color:{PANIC_TEXT_COLOR}; font-size:13px;")
        self.panic_label.setFont(QFont("Courier New", 10))
        self.panic_label.setWordWrap(True)
        self.panic_label.hide()
        root.addWidget(self.panic_label)

        self.game_widgets = [self.header_label, self.grid_frame, self.status_label] + list(
            self.level_buttons.values()
        )

    def _style_buttons(self):
        base = (
            "QPushButton {background:#252526; color:#858585; border:1px solid #3c3c3c;"
            " padding:4px 10px; font-family:'Courier New'; font-size:12px;}"
            " QPushButton:hover {background:#2a2a2a; color:#d4d4d4;}"
        )
        for key, btn in self.level_buttons.items():
            active = key == self.current_level
            style = base
            if active:
                style += " QPushButton {border-color:#4fc1ff; color:#4fc1ff;}"
            btn.setStyleSheet(style)

    # ---------- Game logic ----------

    def change_level(self, level_name):
        self.current_level = level_name
        self._style_buttons()
        self.init_board()

    def init_board(self):
        config = LEVELS[self.current_level]

        # clear old grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.board = [[None for _ in range(config["cols"])] for _ in range(config["rows"])]
        self.cells = [[None for _ in range(config["cols"])] for _ in range(config["rows"])]
        self.game_over = False
        self.first_click = True

        self.header_label.setText(f"// STACK_TRACE_LOG: MINES_LEFT: {config['mines']}")
        self.status_label.setText("> Status: System active.")

        for r in range(config["rows"]):
            for c in range(config["cols"]):
                self.board[r][c] = {
                    "is_mine": False,
                    "is_revealed": False,
                    "is_flagged": False,
                    "count": 0,
                }
                cell = Cell(r, c)
                cell.leftClicked.connect(self.handle_click)
                cell.rightClicked.connect(self.handle_right_click)
                cell.doubleClicked.connect(self.handle_chording)
                self.grid_layout.addWidget(cell, r, c)
                self.cells[r][c] = cell

    def generate_mines(self, start_r, start_c):
        config = LEVELS[self.current_level]
        rows, cols = config["rows"], config["cols"]
        mines_placed = 0
        while mines_placed < config["mines"]:
            r = random.randrange(rows)
            c = random.randrange(cols)
            if not self.board[r][c]["is_mine"] and (
                abs(r - start_r) > 1 or abs(c - start_c) > 1
            ):
                self.board[r][c]["is_mine"] = True
                mines_placed += 1

        for r in range(rows):
            for c in range(cols):
                if self.board[r][c]["is_mine"]:
                    continue
                count = 0
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        nr, nc = r + i, c + j
                        if 0 <= nr < rows and 0 <= nc < cols and self.board[nr][nc]["is_mine"]:
                            count += 1
                self.board[r][c]["count"] = count

    def handle_click(self, r, c):
        if self.game_over or self.board[r][c]["is_flagged"]:
            return
        if self.first_click:
            self.first_click = False
            self.generate_mines(r, c)
        if self.board[r][c]["is_revealed"]:
            self.handle_chording(r, c)
            return
        self.reveal_cell(r, c)

    def handle_right_click(self, r, c):
        if self.game_over or self.board[r][c]["is_revealed"]:
            return
        cell_data = self.board[r][c]
        cell_widget = self.cells[r][c]
        cell_data["is_flagged"] = not cell_data["is_flagged"]
        if cell_data["is_flagged"]:
            cell_widget.render_flagged()
        else:
            cell_widget.render_hidden()

        config = LEVELS[self.current_level]
        flags = sum(
            1
            for row in self.board
            for cell in row
            if cell["is_flagged"]
        )
        self.header_label.setText(
            f"// STACK_TRACE_LOG: MINES_LEFT: {max(0, config['mines'] - flags)}"
        )

    def reveal_cell(self, r, c):
        config = LEVELS[self.current_level]
        rows, cols = config["rows"], config["cols"]
        queue = [(r, c)]

        while queue:
            cr, cc = queue.pop(0)
            if not (0 <= cr < rows and 0 <= cc < cols):
                continue
            cell_data = self.board[cr][cc]
            if cell_data["is_revealed"] or cell_data["is_flagged"]:
                continue

            cell_data["is_revealed"] = True
            cell_widget = self.cells[cr][cc]

            if cell_data["is_mine"]:
                cell_widget.render_mine()
                self.end_game(False)
                return

            cell_widget.count = cell_data["count"]
            cell_widget.render_revealed()

            if cell_data["count"] == 0:
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        nr, nc = cr + i, cc + j
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor = self.board[nr][nc]
                            if not neighbor["is_revealed"] and not neighbor["is_flagged"]:
                                queue.append((nr, nc))

        self.check_win()

    def handle_chording(self, r, c):
        cell_data = self.board[r][c]
        if self.game_over or not cell_data["is_revealed"] or cell_data["count"] == 0:
            return

        config = LEVELS[self.current_level]
        rows, cols = config["rows"], config["cols"]
        flag_count = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                nr, nc = r + i, c + j
                if 0 <= nr < rows and 0 <= nc < cols and self.board[nr][nc]["is_flagged"]:
                    flag_count += 1

        if flag_count == cell_data["count"]:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    nr, nc = r + i, c + j
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor = self.board[nr][nc]
                        if not neighbor["is_revealed"] and not neighbor["is_flagged"]:
                            self.reveal_cell(nr, nc)

    def check_win(self):
        unrevealed_safe = sum(
            1
            for row in self.board
            for cell in row
            if not cell["is_mine"] and not cell["is_revealed"]
        )
        if unrevealed_safe == 0:
            self.end_game(True)

    def end_game(self, is_win):
        self.game_over = True
        self.status_label.setText(
            "> Status: Process complete (0)." if is_win else "> Status: Process terminated (1)."
        )
        for row_idx, row in enumerate(self.board):
            for col_idx, cell_data in enumerate(row):
                cell_widget = self.cells[row_idx][col_idx]
                if cell_data["is_mine"] and not cell_data["is_revealed"]:
                    if cell_data["is_flagged"]:
                        cell_widget.render_flagged()  
                    else:
                        cell_widget.render_mine()
                elif cell_data["is_flagged"] and not cell_data["is_mine"]:
                    cell_widget.render_wrong_flag()  


    def toggle_panic(self):
        self.is_panicked = not self.is_panicked
        for widget in self.game_widgets:
            widget.setVisible(not self.is_panicked)
        self.panic_label.setVisible(self.is_panicked)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(420, 420)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
