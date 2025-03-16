from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

def create_header():
    header_widget = QWidget()
    header_widget.setFixedHeight(80)  # Standard height for all headers
    header_widget.setStyleSheet("background-color: #004d00;")  # Green background

    header_layout = QHBoxLayout(header_widget)
    header_layout.setContentsMargins(10, 10, 10, 10)
    header_layout.setSpacing(10)

    # Logo
    logo_label = QLabel()
    logo_pixmap = QPixmap("BM_moters.png")  # Ensure this path is correct
    if logo_pixmap.isNull():
        logo_pixmap = QPixmap(100, 60)
        logo_pixmap.fill(Qt.GlobalColor.gray)

    # Correct usage of scaled method
    scaled_logo = logo_pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    logo_label.setPixmap(scaled_logo)
    header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

    # Header Text
    header_text = QLabel("BISMILLAH MOTORS")
    header_text.setStyleSheet("color: white;")
    header_font = QFont("Arial", 24, QFont.Weight.Bold)
    header_text.setFont(header_font)
    header_layout.addStretch(1)
    header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
    header_layout.addStretch(1)

    return header_widget
