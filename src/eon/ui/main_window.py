
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
)


class MainWindow(QMainWindow):
    BG = "#0b0d12"
    SIDEBAR = "#10131b"
    PANEL = "#141722"
    BORDER = "#282d3b"
    TEXT = "#e6e8ef"
    MUTED = "#858b9d"
    ACCENT = "#7888ff"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EON — Personal AI Agent")
        self.resize(1200, 760)
        self.setMinimumSize(900, 600)

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {self.BG};
                color: {self.TEXT};
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 14px;
            }}

            QFrame#sidebar {{
                background-color: {self.SIDEBAR};
                border-right: 1px solid {self.BORDER};
            }}

            QLabel#brand {{
                font-size: 26px;
                font-weight: 700;
                color: #a5b4fc;
            }}

            QLabel#muted {{
                color: {self.MUTED};
                font-size: 12px;
            }}

            QLabel#heading {{
                font-size: 19px;
                font-weight: 600;
            }}

            QPushButton {{
                background-color: #191d28;
                color: {self.TEXT};
                border: 1px solid {self.BORDER};
                border-radius: 9px;
                padding: 11px;
                text-align: left;
            }}

            QPushButton:hover {{
                background-color: #242a3a;
                border-color: #505b80;
            }}

            QPushButton#primary {{
                background-color: {self.ACCENT};
                color: #0b0d12;
                font-weight: 700;
                border: none;
                padding: 12px 18px;
            }}

            QPushButton#primary:hover {{
                background-color: #9ba6ff;
            }}

            QPushButton#small {{
                padding: 7px 10px;
                background-color: transparent;
                border: none;
                color: {self.MUTED};
            }}

            QLineEdit {{
                background-color: {self.PANEL};
                color: {self.TEXT};
                border: 1px solid #303547;
                border-radius: 11px;
                padding: 14px;
                selection-background-color: #5968c9;
            }}

            QLineEdit:focus {{
                border: 1px solid {self.ACCENT};
            }}

            QScrollArea {{
                background-color: {self.BG};
                border: none;
            }}

            QScrollBar:vertical {{
                background-color: {self.BG};
                width: 8px;
                margin: 0;
            }}

            QScrollBar::handle:vertical {{
                background-color: #34394b;
                border-radius: 4px;
                min-height: 25px;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        side = QVBoxLayout(sidebar)
        side.setContentsMargins(16, 24, 16, 18)
        side.setSpacing(12)

        brand = QLabel("EON")
        brand.setObjectName("brand")

        tagline = QLabel("YOUR PERSONAL AI")
        tagline.setObjectName("muted")

        new_chat = QPushButton("+   New conversation")
        conversations = QPushButton("◷   Conversations")
        memory = QPushButton("◇   Memory")
        tools = QPushButton("⌘   Tools")
        settings = QPushButton("⚙   Settings")

        new_chat.clicked.connect(self.new_conversation)
        conversations.clicked.connect(self.show_conversations)
        memory.clicked.connect(lambda: self.show_notice(
            "Memory", "Persistent memory will be implemented in a later phase."
        ))
        tools.clicked.connect(lambda: self.show_notice(
            "Agent tools", "Approved agent tools will be implemented later."
        ))
        settings.clicked.connect(self.show_settings)

        side.addWidget(brand)
        side.addWidget(tagline)
        side.addSpacing(20)
        side.addWidget(new_chat)
        side.addWidget(conversations)
        side.addWidget(memory)
        side.addWidget(tools)
        side.addStretch()
        side.addWidget(settings)

        # Main workspace
        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 18)
        content_layout.setSpacing(16)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        heading = QLabel("Your workspace")
        heading.setObjectName("heading")

        subtitle = QLabel("A personal assistant designed around you.")
        subtitle.setObjectName("muted")

        title_box.addWidget(heading)
        title_box.addWidget(subtitle)

        self.status = QLabel("●  UI ready · Gemini not connected")
        self.status.setObjectName("muted")

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignTop)

        # Conversation area
        self.chat_area = QWidget()
        self.chat_area.setObjectName("chatArea")
        self.chat_area.setStyleSheet(
            f"QWidget#chatArea {{ background-color: {self.BG}; }}"
        )

        self.chat_layout = QVBoxLayout(self.chat_area)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        self.chat_layout.setSpacing(18)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("chatScroll")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setStyleSheet(f"""
            QScrollArea#chatScroll {{
                background-color: {self.BG};
                border: none;
            }}
            QScrollArea#chatScroll QWidget#qt_scrollarea_viewport {{
                background-color: {self.BG};
                border: none;
            }}
        """)
        self.scroll.viewport().setAutoFillBackground(True)
        self.scroll.setWidget(self.chat_area)

        # Message composer
        composer = QFrame()
        composer.setStyleSheet(f"""
            QFrame {{
                background-color: {self.SIDEBAR};
                border: 1px solid {self.BORDER};
                border-radius: 14px;
            }}
        """)

        composer_layout = QHBoxLayout(composer)
        composer_layout.setContentsMargins(12, 10, 12, 10)
        composer_layout.setSpacing(10)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message EON...")
        self.message_input.setClearButtonEnabled(True)
        self.message_input.returnPressed.connect(self.send_message)

        send_button = QPushButton("Send  ↗")
        send_button.setObjectName("primary")
        send_button.clicked.connect(self.send_message)

        composer_layout.addWidget(self.message_input, 1)
        composer_layout.addWidget(send_button)

        footer = QLabel(
            "Prototype mode · Messages are not saved between sessions."
        )
        footer.setObjectName("muted")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addLayout(header)
        content_layout.addWidget(self.scroll, 1)
        content_layout.addWidget(composer)
        content_layout.addWidget(footer)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, 1)

        self.setCentralWidget(root)

    def _show_welcome(self):
        welcome_box = QWidget()
        welcome_box.setStyleSheet(
            f"QWidget {{ background-color: {self.BG}; }}"
        )

        layout = QVBoxLayout(welcome_box)
        layout.setContentsMargins(20, 35, 20, 25)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel("✳")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(
            "font-size: 42px; color: #a5b4fc; background: transparent;"
        )

        title = QLabel("Welcome to EON")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 27px; font-weight: 700; background: transparent;"
        )

        description = QLabel(
            "Your personal AI companion starts here.\n"
            "A new space to think, plan, and get things done."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet(
            f"font-size: 14px; color: {self.MUTED}; "
            "background: transparent; line-height: 1.5;"
        )

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(description)

        self.chat_layout.addWidget(welcome_box)

    def _add_message(self, text, sender):
        row = QWidget()
        row.setStyleSheet("background: transparent;")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        bubble.setMaximumWidth(650)
        bubble.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum
        )

        if sender == "user":
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #252b40;
                    color: #f1f3f9;
                    border: 1px solid #353e5b;
                    border-radius: 14px;
                    padding: 13px 16px;
                }
            """)
            row_layout.addStretch()
            row_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet(f"""
                QLabel {{
                    background-color: {self.SIDEBAR};
                    color: {self.TEXT};
                    border: 1px solid {self.BORDER};
                    border-radius: 14px;
                    padding: 13px 16px;
                }}
            """)
            row_layout.addWidget(bubble)
            row_layout.addStretch()

        self.chat_layout.addWidget(row)
        QTimer.singleShot(
            0,
            lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            ),
        )

    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return

        # Remove the welcome screen on the first message.
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self._add_message(message, "user")
        self.message_input.clear()

        self._add_message(
            "The interface is working. Gemini has not been connected yet.",
            "assistant",
        )

    def new_conversation(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self._show_welcome()
        self.message_input.clear()

    def show_notice(self, title, message):
        self._add_message(f"{title}: {message}", "assistant")

    def show_conversations(self):
        self.show_notice(
            "Conversations",
            "Conversation history will be added when persistence is implemented.",
        )

    def show_settings(self):
        self.show_notice(
            "Settings",
            "Configuration and API settings will be added in a later step.",
        )
