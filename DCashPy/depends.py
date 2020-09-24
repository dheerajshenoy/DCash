import kivymd
from table import TableButton
from math import inf
from kivymd.app import MDApp
from kivymd.uix.spinner import MDSpinner
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton, MDRoundFlatIconButton, MDRaisedButton, MDTextButton, MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.list import MDList, OneLineIconListItem, TwoLineListItem, IconLeftWidget, OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemeManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.banner import MDBanner
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from datetime import date
import time
import csv
import shutil
import notify2
import os

from Screen import *
sm = ScreenManager()
