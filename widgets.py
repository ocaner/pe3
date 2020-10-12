#!/usr/bin/env python3

from PyQt5.Qt import QColor, QBrush, QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from copy import copy
from dataclasses import fields

"""

        self.table = QTableWidget(len(self.pe3.cpu.GPR), 2)

        vertLabels = []

        fs = fields(self.pe3.cpu.GPR)

        for i in range(len(self.pe3.cpu.GPR)):
            vertLabels.append(fs[i].name)

        self.table.setHorizontalHeaderLabels(["Dec", "Hex"])
        self.table.setVerticalHeaderLabels(vertLabels)    
        self.table.setMaximumWidth(350)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
"""        

class  QRegistersWidget(QTableWidget):

    HEADERS = ["Hex", "Dec", "Bin"]

    def __init__(self, registers):
        super().__init__(len(registers), len(QRegistersWidget.HEADERS))
        self.registers = registers
        self.labels = None
        self.values = None
        self.old_background = None
        self.old_foreground = None
        self.black = QBrush(QColor("#000000"))
        self.change = QBrush(QColor("#c0c000"))
        self.mono = QFont("Cascadia Code PL", 16)

        self.init_ui()

    def init_ui(self):
        self.setHorizontalHeaderLabels(QRegistersWidget.HEADERS)
        self.setMaximumWidth(600)
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 250)

        fs = fields(self.registers)
        self.count = len(fs)
        self.labels = [fs[i].name for i in range(self.count) ]
        self.setVerticalHeaderLabels(self.labels)
        
    def snapshot(self):
        self.values = copy(self.registers)

    def update(self):
        for i in range(self.count):
            old_value = self.values[i]
            new_value = self.registers[i]

            x = self.item(i, 0)
            d = self.item(i, 1)
            b = self.item(i, 2)
            
            if x is None:
                x = QTableWidgetItem("", 1)
                x.setFont(self.mono)
                self.setItem(i, 0, x)

            if d is None:
                d = QTableWidgetItem("", 1)
                d.setFont(self.mono)
                self.setItem(i, 1, d)
            
            if b is None:
                b = QTableWidgetItem("", 1)
                b.setFont(self.mono)
                self.setItem(i, 2, b)
            
            x.setText(f"{new_value:08x}")
            d.setText(f"{new_value:d}")
            b.setText(f"{new_value:32b}")
            #self.table.setCellWidget(i, 0, d)
            #self.table.setCellWidget(i, 1, x)
            
            #di = self.table.itemAt(i, 0)
            #xi = self.table.itemAt(i, 1)

            if old_value != new_value:
                if self.old_background is None:
                    self.old_background = d.background()
                
                if self.old_foreground is None:
                    self.old_foreground = d.foreground()

                x.setForeground(self.black)
                x.setBackground(self.change)

                d.setForeground(self.black)
                d.setBackground(self.change)

                b.setForeground(self.black)
                b.setBackground(self.change)
            else:
                if self.old_background is not None:
                    x.setBackground(self.old_background)
                    d.setBackground(self.old_background)
                    b.setBackground(self.old_background)
                
                if self.old_foreground is not None:
                    x.setForeground(self.old_foreground)
                    d.setForeground(self.old_foreground)
                    b.setForeground(self.old_foreground)