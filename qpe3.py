#!/usr/bin/env python3

from PyQt5.Qt import QColor, QBrush, QFont, QIcon, QStyle, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTextEdit, QAction, QLabel, QTableWidgetItem, QTabWidget

from copy import copy
from dataclasses import fields

from pe3 import PE3
from cpu import R5900
from widgets import QRegistersWidget

class Callback(object):

    def callback(self, addr, op, mn):
        pass

class LogCallback(Callback):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def callback(self, addr, op, mn):
        self.widget.setText(f"{addr:08x} {op:08x}\n\t{mn}")

BIOSES={
    "USA 1.0": "",
    "Japan"
}

class QPE3Window(QWidget):

    def __init__(self):
        super().__init__()
        self.pe3 = PE3()
        self.pe3.cpu.callback = self
        self.mono = QFont("Cascadia Code PL", 16)
        self.oldbg = None
        self.oldfg = None
        self.initUI()

    def opcode_error(self, addr, op, mn, error):
        self.opcode_callback(addr, op, mn, error=True, errormsg=error)

    def opcode_success(self, addr, op, mn):
        self.opcode_callback(addr, op, mn)

    def opcode_callback(self, addr, op, mn, error=False, errormsg=None):
        #t = self.text.toHtml()
        #self.text.setText( t + self.TEMPLATE.format(addr=addr,op=op,mn=mn))
        y = self.ops.rowCount()
        self.ops.setRowCount(y + 1)
        #self.ops.rowCount += 1

        print(f"{'✓' if not error else '✗'} {addr:08x} {op:08x} {mn}")
        
        s = QTableWidgetItem("✓" if not error else "✗")
        a = QTableWidgetItem(f"{addr:08x}", 1)
        a.setFont(self.mono)
        b = QTableWidgetItem(f"{op:08x}", 1)
        b.setFont(self.mono)
        
        
        c = QTableWidgetItem(f"{errormsg}" if error and errormsg else f"{mn}", 1)
        
        c.setFont(self.mono)
        d = QTableWidgetItem(f"{op:032b}", 1)
        d.setFont(self.mono)

        if error:
            for x in (a, b, c, s):
                x.setForeground(self.normal)
                x.setBackground(self.error)
        else:
            s.setForeground(self.success)

        self.ops.setItem(y, 0, a)
        self.ops.setItem(y, 1, b)
        self.ops.setItem(y, 2, s)
        self.ops.setItem(y, 3, c)
        self.ops.setItem(y, 4, d)
        #self.ops.setCurrentCell(y, 3)        
        self.ops.scrollToItem(a, hint=True)
        self.ops.scrollToItem(a)

        if error:
            print("Stop!!!")
            self.running = False

    def initUI(self):
        self.layout = QVBoxLayout()
        #self.table = QTableWidget(len(self.pe3.cpu.GPR), 2)
        self.black = QBrush(QColor("#000000"))
        self.change = QBrush(QColor("#c0c000"))
        self.normal = QBrush(QColor("#ffffff"))
        self.error = QBrush(QColor("#e00000"))
        self.success = QBrush(QColor("#00e000"))
        self.run = QPushButton("Run")
        self.run.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
        self.next = QPushButton("Next")
        self.next.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MediaSeekForward")))
        #setIcon(QIcon("SP_MediaSeekForward"))
        self.next.setEnabled(False)
        self.buttons = QWidget()
        self.vlayout = QHBoxLayout()
        

        self.runSteps = QPushButton("Run Steps")
        self.btnPause = QPushButton("Pause")
        self.btnPause.setEnabled(False)
        self.btnPause.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MediaPause")))
        #self.reset
        self.vlayout.addWidget(self.run)
        self.vlayout.addWidget(self.runSteps)
        self.vlayout.addWidget(self.btnPause)
        self.vlayout.addWidget(self.btnPause)
        self.vlayout.addWidget(self.next)
        self.buttons.setLayout(self.vlayout)
        self.layout.addWidget(self.buttons)
        self.regtabs = QTabWidget()
        self.regtabs.setMaximumWidth(350)
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        self.layout.addWidget(widget)
    
        self.gpr = QRegistersWidget(self.pe3.cpu.GPR)
        self.cpr = QRegistersWidget(self.pe3.cpu.CPR)
        #self.regtabs.addTab(self.table, "GPR")
        self.regtabs.addTab(self.gpr, "GPR")
        self.regtabs.addTab(self.cpr, "CPR")

        layout.addWidget(self.regtabs)
        #layout.addWidget(self.table)
        # vertLabels = []

        # fs = fields(self.pe3.cpu.GPR)

        # for i in range(len(self.pe3.cpu.GPR)):
        #     vertLabels.append(fs[i].name)

        # self.table.setHorizontalHeaderLabels(["Dec", "Hex"])
        # self.table.setVerticalHeaderLabels(vertLabels)    
        # self.table.setMaximumWidth(350)
        # self.table.setColumnWidth(0, 150)
        # self.table.setColumnWidth(1, 150)
        #run.hitButto
        self.ops = QTableWidget(0, 5)
        self.ops.setHorizontalHeaderLabels(["Address", "Op Code", "Status", "Mnenomic", "Op Code (Bin)"])
        self.ops.setColumnWidth(0, 200)
        self.ops.setColumnWidth(1, 200)
        self.ops.setColumnWidth(2, 50)
        self.ops.setColumnWidth(3, 400)
        self.ops.setColumnWidth(4, 400)
        self.ops.setAutoScroll(True)
        layout.addWidget(self.ops)
        self.setLayout(self.layout)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("qPEEE")

        self.run.clicked.connect(self.onRun)
        self.next.clicked.connect(self.onNext)
        self.btnPause.clicked.connect(self.onPause)

        self.timer = QTimer()
        self.timer.setInterval(125)
        self.timer.timeout.connect(self.onCycle)

    def cycle(self):
        print(f"<<>> CYCLE {self.pe3.cpu.GPR.PC:08x}")
        self.gpr.snapshot()
        self.cpr.snapshot()

        #pre = copy(self.pe3.cpu.GPR)

        addr = self.pe3.cpu.GPR.PC
        size = self.pe3.cpu.cycle(addr)

        #if size != -1:
        #    #self.pe3.cpu.GPR.set(R5900.PC, addr + size)
        #    self.pe3.cpu.GPR.PC = addr + size

        self.gpr.update()
        self.cpr.update()

        # for i in range(len(self.pe3.cpu.GPR)):
        #     d = self.table.item(i, 0)
        #     x = self.table.item(i, 1)
            
        #     if d is None:
        #         d = QTableWidgetItem("", 1)
        #         d.setFont(self.mono)
        #         self.table.setItem(i, 0, d)
            
        #     if x is None:
        #         x = QTableWidgetItem("", 1)
        #         x.setFont(self.mono)
        #         self.table.setItem(i, 1, x)

        #     v = self.pe3.cpu.GPR[i]
        #     d.setText(f"{v:d}")
        #     x.setText(f"{v:08x}")
        #     #self.table.setCellWidget(i, 0, d)
        #     #self.table.setCellWidget(i, 1, x)
            
        #     #di = self.table.itemAt(i, 0)
        #     #xi = self.table.itemAt(i, 1)

        #     if v != pre[i]:
        #         if self.oldbg is None:
        #             self.oldbg = d.background()
                
        #         if self.oldfg is None:
        #             self.oldfg = d.foreground()
        #         #self.old =
        #         d.setForeground(self.black)
        #         x.setForeground(self.black)
        #         d.setBackground(self.change)
        #         x.setBackground(self.change)
        #     else:
        #         if self.oldbg is not None:
        #             d.setBackground(self.oldbg)
        #             x.setBackground(self.oldbg)
        #         if self.oldfg is not None:
        #             d.setForeground(self.oldfg)
        #             x.setForeground(self.oldfg)


    def stop(self):
        self.run.setEnabled(True)
        self.next.setEnabled(False)
        self.timer.stop()

    def reset(self):
        self.stop()

    def onCycle(self):
        if not self.running:
            self.stop()
            return
        
        self.cycle()

    def onReset(self):
        pass

    def onPause(self):
        self.run.setEnabled(True)
        self.btnPause.setEnabled(False)
        self.stop()

    def onNext(self):
        self.cycle()
        
    def onRun(self):
        self.run.setEnabled(False)
        self.next.setEnabled(True)
        self.btnPause.setEnabled(True)
        
        self.running = True
        self.timer.start()
        #while self.running:
        #    self.cycle()


if __name__ == "__main__":
    app = QApplication([])
    window = QPE3Window()
    window.show()
    app.exec_()