import sys
import requests
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, projection='3d')
        super(MplCanvas, self).__init__(self.fig)

class UcusUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İHA Takım Rota Takibi")
        self.setGeometry(100, 100, 1000, 750)

        main_widget = QWidget()
        self.layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        input_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Takım Numarası Girin (Örn: 2, 5, 18)...")
        self.search_btn = QPushButton("Sorgula ve Rotayı Çiz")
        self.search_btn.clicked.connect(self.get_flight_data)
        
        input_layout.addWidget(QLabel("Takım No:"))
        input_layout.addWidget(self.id_input)
        input_layout.addWidget(self.search_btn)
        self.layout.addLayout(input_layout)

        self.info_label = QLabel("Bilgi: Sorgu bekleniyor...")
        self.info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;")
        self.layout.addWidget(self.info_label)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.layout.addWidget(self.canvas)

    def get_flight_data(self):
        team_id = self.id_input.text()
        if not team_id.isdigit():
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayısal Takım No girin.")
            return

        try:
            response = requests.get(f"http://127.0.0.1:5000/flight/{team_id}")
            if response.status_code == 200:
                res_data = response.json()
                self.draw_route(res_data['data'])
            else:
                QMessageBox.warning(self, "Bulunamadı", f"Takım {team_id} için veri bulunamadı.")
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Flask sunucusuna ulaşılamadı: {e}")

    def draw_route(self, coords):
        lats = [c['lat'] for c in coords]
        lons = [c['lon'] for c in coords]
        alts = [c['alt'] for c in coords]

        self.canvas.axes.cla()
  
        self.canvas.axes.plot(lons, lats, alts, marker='o', markersize=4, color='darkblue', linestyle='--')
        
        self.canvas.axes.xaxis.get_major_formatter().set_useOffset(False)
        self.canvas.axes.yaxis.get_major_formatter().set_useOffset(False)

        for label in self.canvas.axes.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('right') 
            
        for label in self.canvas.axes.get_yticklabels():
            label.set_rotation(-15) 
        
        self.canvas.axes.set_xlabel('Boylam', labelpad=40, fontweight='bold', color='darkred') 
        self.canvas.axes.set_ylabel('Enlem', labelpad=25, fontweight='bold')
        self.canvas.axes.set_zlabel('İrtifa', labelpad=15, fontweight='bold')
        
        self.canvas.draw()

        start_p = f"({lats[0]:.4f}, {lons[0]:.4f})"
        end_p = f"({lats[-1]:.4f}, {lons[-1]:.4f})"
        self.info_label.setText(f"✅ Veri Çizildi | Başlangıç: {start_p} | Bitiş: {end_p}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UcusUygulamasi()
    window.show()
    sys.exit(app.exec_())