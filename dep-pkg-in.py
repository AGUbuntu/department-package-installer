import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QLineEdit, QDialog, QDialogButtonBox

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enter Sudo Password')

        self.password_label = QLabel('Please enter your sudo password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask input for password

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_password(self):
        if self.exec() == QDialog.Accepted:
            return self.password_input.text()
        return None

class PackageInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Department Package Installer')

        self.package_groups = {
            'Computer Engineering': ['codium', 'octave', 'scrcpy'],
            'Civil Engineering': ['librecad', 'librecad-data', 'blender', 'krita'],
            'Electrical & Electronics Engineering': ['codium', 'octave', 'kicad'],
            'Industrial Engineering': ['librecad', 'librecad-data', 'blender', 'krita', 'kicad', 'octave'],
            'Mechanical Engineering': ['librecad', 'librecad-data', 'blender', 'krita', 'kicad', 'octave', 'codium'],
            'Architecture': ['librecad', 'librecad-data', 'blender', 'krita']
        }

        self.package_groups_label = QLabel('Select your department package group to install:')
        self.install_button = QPushButton('Install Packages')
        self.install_button.clicked.connect(self.install_packages)

        layout = QVBoxLayout()
        layout.addWidget(self.package_groups_label)

        self.checkbox_group = []
        for group, packages in self.package_groups.items():
            group_checkbox = QCheckBox(group)
            group_checkbox.packages = packages
            layout.addWidget(group_checkbox)
            self.checkbox_group.append(group_checkbox)

        layout.addWidget(self.install_button)

        self.setLayout(layout)

    def install_packages(self):
        password_dialog = PasswordDialog()
        sudo_password = password_dialog.get_password()

        if not sudo_password:
            QMessageBox.warning(self, 'Warning', 'Please enter the sudo password before installing packages.')
            return

        # Perform a one-time system update
        update_command = 'sudo -S apt update'
        update_process = subprocess.Popen(['bash', '-c', update_command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        update_process.communicate(input=f'{sudo_password}\n'.encode())

        groups_to_install = [checkbox for checkbox in self.checkbox_group if checkbox.isChecked()]

        for group in groups_to_install:
            packages_command = ' '.join(group.packages)
            command = f'sudo -S apt install -y {packages_command}'
            process = subprocess.Popen(['bash', '-c', command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(input=f'{sudo_password}\n'.encode())

        # Show installation completed message
        QMessageBox.information(self, 'Installation Completed', 'Packages installed successfully.')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    package_installer = PackageInstaller()
    package_installer.show()
    sys.exit(app.exec())
