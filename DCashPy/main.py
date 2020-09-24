from depends import *

notify2.init("DCash") # NOTIFICATION DAEMON INITIALIZATION
n = notify2.Notification(None, icon="")

# INITIAL PROGRAM LAUNCH SETTINGS
mainFolder = ""
folderName = "DCashDocX"
logName = "logDCash.txt"
taxlist =["CGST@0%", "Exempted", "IGST@0%", "SGST@0%", "CGST@0.125%", "SGST@0.125%", "IGST@0.25%"]
primary_units = ["BTL", "PKT", "STP", "BOX", "PKG"]
secondary_units = ["gm", "kg", "ml", "caps", "tab", "no."]

# GLOBAL VARIABLES FOR UNIT SELECTIONS
primaryUnitSelected = ""
secondaryUnitSelected = ""
unitMultiplierSelected = ""

# CSV FILE HOLDERS
ITEMS = [] # ENTIRE ITEMS FILE CSV LIST HOLDER
PARTIES = []
ITEM_CONTAINER = []
ITEMS_NAME = []		# ITEM NAMES
ITEMS_UNIT_MULTIPLIER = []		# UNIT MULTIPLIERS
ITEMS_SECONDARY_UNIT = []		# SECONDARY UNITS

# BOOLEAN FOR DETECTING NEW ITEMS ADDED
itemListChanged = False
partyListChanged = False


# LAYOUT FOR INITIAL FOLDER CREATION DIALOG
class folder_dialog_layout(MDBoxLayout):
    global mainFolder
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p = ""
        self.ids.folder_selected_label.text = '/'

    def FM(self):
        self.file_manager_widget = MDFileManager(select_path=self.get_def_dir, exit_manager=self.exit_manager)
        self.file_manager_widget.show('/')

    def get_def_dir(self, path):
        global mainFolder
        mainFolder = path
        if(path != "" or path != "/"):
            self.ids.folder_ok_btn.disabled = False
        self.ids.folder_selected_label.text = str(path)
        self.file_manager_widget.close()

    def exit_manager(self, *args):
        self.file_manager_widget.close()

    def folder_ok(self):
        DCash().closeSaveDialog()


# MAIN SCREEN
class Main(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        navlayout = MDBoxLayout(orientation='vertical')
        navDrawer = MDNavigationDrawer(radius=[0,0,0,0])
        toolbar = MDToolbar(title="DCash", elevation=0)
        toolbar.left_action_items = [["menu",lambda x: navDrawer.set_state("open")]]
        toolbar.right_action_items = [["dots-vertical",lambda x: navDrawer.set_state("open")]]

        sm.add_widget(ItemScreen(name="itemscreen"))
        sm.add_widget(PartyScreen(name="partyscreen"))
        sm.add_widget(HomeScreen(name="homescreen"))
        sm.add_widget(InventoryScreen(name="inventoryscreen"))
        sm.add_widget(PurchaseScreen(name="purchasescreen"))
        sm.add_widget(HistoryScreen(name="historyscreen"))
        sm.add_widget(SettingScreen(name="settingscreen"))

        sm.add_widget(NewItemScreen(name="newitemscreen"))
        sm.add_widget(NewPartyScreen(name="newpartyscreen"))

        sm.current = "homescreen"

        navlayout.add_widget(toolbar)
        navDrawerContent = MDGridLayout(cols=1)

        btnList = MDList()

        closeBtn = OneLineIconListItem(text="", on_release = lambda x: navDrawer.set_state("close"))
        closeBtnIcon = IconLeftWidget(icon="close")
        closeBtn.add_widget(closeBtnIcon)

        homeBtn = OneLineIconListItem(text="Home",on_release = lambda x: self.ChangeScreen("homescreen"))
        homeBtnIcon = IconLeftWidget(icon="home")
        homeBtn.add_widget(homeBtnIcon)

        inventoryBtn = OneLineIconListItem(text="Inventory", on_release = lambda x: self.ChangeScreen("inventoryscreen"))
        inventoryBtnIcon = IconLeftWidget(icon="archive")
        inventoryBtn.add_widget(inventoryBtnIcon)

        partyBtn = OneLineIconListItem(text="Parties", on_release = lambda x: self.ChangeScreen("partyscreen"))
        partyBtnIcon = IconLeftWidget(icon="account")
        partyBtn.add_widget(partyBtnIcon)

        itemBtn = OneLineIconListItem(text="Items", on_release = lambda x: self.ChangeScreen("itemscreen"))
        itemBtnIcon = IconLeftWidget(icon="inbox")
        itemBtn.add_widget(itemBtnIcon)

        purchaseBtn = OneLineIconListItem(text="Purchase", on_release = lambda x: self.ChangeScreen("purchasescreen"))
        purchaseBtnIcon = IconLeftWidget(icon="download")
        purchaseBtn.add_widget(purchaseBtnIcon)

        historyBtn = OneLineIconListItem(text="History",on_release = lambda x: self.ChangeScreen("historyscreen"))
        historyBtnIcon = IconLeftWidget(icon="history")
        historyBtn.add_widget(historyBtnIcon)

        settingsBtn= OneLineIconListItem(text="Settings",on_release = lambda x: self.ChangeScreen("settingscreen"))
        settingsBtnIcon = IconLeftWidget(icon="apps")
        settingsBtn.add_widget(settingsBtnIcon)

        btnList.add_widget(closeBtn)
        btnList.add_widget(homeBtn)
        btnList.add_widget(inventoryBtn)
        btnList.add_widget(partyBtn)
        btnList.add_widget(itemBtn)
        btnList.add_widget(purchaseBtn)
        btnList.add_widget(historyBtn)
        btnList.add_widget(settingsBtn)

        navDrawerContent.add_widget(btnList)
        navDrawer.add_widget(navDrawerContent)
        navlayout.add_widget(sm)
        self.add_widget(navlayout)
        self.add_widget(navDrawer)

    def ChangeScreen(self, ScreenName):
            sm.current = ScreenName
            sm.transition.direction = "left"

itemNameHelper = """
MDTextField:
    hint_text: "Item Name *"
    write_tab: False
    multiline: False
    size_hint_x: 0.8
    helper_text: "This field is required"
    helper_text_mode: "on_focus"
"""

batchNumberHelper = """
MDTextField:
    hint_text: "Batch Number"
    multiline: False
    write_tab: False
"""

companyNameHelper = """
MDTextField:
    hint_text: "Company Name *"
    write_tab: False
    size_hint: 0.7, None
    multiline: False
    helper_text: "This field is required"
    helper_text_mode: "on_focus"

"""
salePriceHelper = """
MDTextField:
    hint_text: "Sale Price *"
    write_tab: False
    multiline: False
    size_hint_x : 0.8
    helper_text: "This field is required"
    helper_text_mode: "on_focus"

"""
purchasePriceHelper = """
MDTextField:
    hint_text: "Purchase Price *"
    write_tab: False
    multiline: False
    size_hint_x : 0.8
    helper_text: "This field is required"
    helper_text_mode: "on_focus"

"""
openingStockHelper = """
MDTextField:
    hint_text: "Opening Stock"
    write_tab: False
    multiline: False
    size_hint_x : 0.4
    helper_text: "Initial Stock of item"
    helper_text_mode: "on_focus"

"""

unitMultiplierHelper = """
MDTextField:
    size_hint_x: None
    width: "40dp"
    multiline: False

"""
# LAYOUT FOR THE UNIT SELECTION DIALOG
class unit_dialog_layout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if(os.path.exists(MAINPATH + '/primary_units') and os.path.exists(MAINPATH + '/secondary_units')):
            pass
        else:
            with open(MAINPATH + '/primary_units','w') as f:
                for i in primary_units:
                    f.write(i + '\n')
            with open(MAINPATH + '/secondary_units','w') as f:
                for i in secondary_units:
                    f.write(i + '\n')
        
        self.orientation = 'vertical'
        self.padding = "10dp"
        self.spacing = "10dp"

        self.secondlayout = MDGridLayout(cols=3, spacing="2dp", padding="4dp")

        self.primaryBtn = MDRaisedButton(text="Select Primary Unit", on_release = lambda x: self.showPrimaryDropDown())
        self.primaryUnitLabel = MDLabel(size_hint=(None,0.2))

        self.unitMultiplier = Builder.load_string(unitMultiplierHelper)
        self.unitMultiplier.bind(focus=self.getUnitMultiplier)

        self.secondaryBtn = MDRaisedButton(text="Select Secondary Unit", on_release = lambda x: self.showSecondaryDropDown())
        self.secondaryUnitLabel = MDLabel(size_hint=(None,0.2))

        self.primaryDropDown = DropDown(auto_width=False, width=self.primaryBtn.width + 50)

        with open(MAINPATH + '/primary_units','r') as f:
            lines = f.readlines()
            for line in lines:
                btn = MDRaisedButton(text=line.strip(), on_release=self.getPrimaryUnit)
                self.primaryDropDown.add_widget(btn)


        self.secondaryDropDown = DropDown(auto_width=False, width= self.secondaryBtn.width + 50)
        with open(MAINPATH + '/secondary_units','r') as f:
            lines = f.readlines()
            for line in lines:
                btn = MDRaisedButton(text=line.strip(), on_release=self.getSecondaryUnit)
                self.secondaryDropDown.add_widget(btn)
        
        self.secondlayout.add_widget(self.primaryUnitLabel)
        self.secondlayout.add_widget(self.unitMultiplier)
        self.secondlayout.add_widget(self.secondaryUnitLabel)
        
        self.add_widget(self.secondlayout)
        self.add_widget(self.primaryBtn)
        self.add_widget(self.secondaryBtn)


# GET PRIMARYUNIT FROM DROPDOWN SELECTION
    def getPrimaryUnit(self, pu):
        global primaryUnitSelected
        primaryUnitSelected = pu.text
        self.primaryUnitLabel.text = str(primaryUnitSelected) + " = "

# GET SECONDARYUNIT FROM DROPDOWN SELECTION
    def getSecondaryUnit(self, su):
        global secondaryUnitSelected
        secondaryUnitSelected = su.text
        self.secondaryUnitLabel.text = str(secondaryUnitSelected)

# DISPLAYING PRIMARY UNIT DROPDOWN
    def showPrimaryDropDown(self):
        self.primaryDropDown.open(self.primaryBtn)

# DISPLAYING SECONDARY UNIT DROPDOWN
    def showSecondaryDropDown(self):
        self.secondaryDropDown.open(self.secondaryBtn)

# GET UNIT MULTIPLIER
    def getUnitMultiplier(self, instance, value):
        global unitMultiplierSelected
        if value:
            pass
        else:
            unitMultiplierSelected = instance.text

class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDGridLayout(cols=2,padding="5dp",spacing="5dp")
        leftbar = MDGridLayout(rows=2,cols=1,spacing="6dp",size_hint_x=0.4)

        card1 = MDCard(size_hint_y=0.19,elevation=3)
        card2 = MDCard(elevation=3)
        card3 = MDCard(elevation=0)

        card1layout = MDGridLayout(rows=4,padding="2dp",spacing="2dp")
        card1innerlayout = MDBoxLayout(spacing="2dp", padding="2dp")

        self.itemsLabel = MDLabel(text="", size_hint=(1,None), size=("40dp","40dp"),font_style="H5")
        sortBtn = MDIconButton(icon="filter", size_hint=(None,None),size=("20dp","20dp"))
        searchBtn = MDIconButton(icon="android",size_hint=(None,None), size=("20dp","20dp"))
        partyBtn = MDRaisedButton(text="+ ITEM", on_release= lambda x: self.addItem())


        card1innerlayout.add_widget(self.itemsLabel)
        card1innerlayout.add_widget(sortBtn)
        card1innerlayout.add_widget(searchBtn)

        card1layout.add_widget(card1innerlayout)
        card1layout.add_widget(partyBtn)


        self.card2layoutScrollView = ScrollView(bar_width=4, bar_inactive_color=[.7,.7,.7,.5])
        
        self.card2layout = MDGridLayout(cols=1, size_hint_y=None)
        self.card2layout.bind(minimum_height=self.card2layout.setter('height'))

        self.card2layoutScrollView.add_widget(self.card2layout)

        card3layout = MDGridLayout()

        card1.add_widget(card1layout)
        card2.add_widget(self.card2layoutScrollView)
        card3.add_widget(card3layout)

        leftbar.add_widget(card1)
        leftbar.add_widget(card2)


        layout.add_widget(leftbar)
        layout.add_widget(card3)
        self.add_widget(layout)

        global ITEMS

        if(os.path.exists(MAINPATH + '/items')):
            with open(MAINPATH + '/items', 'r') as f:
                csv_reader = csv.DictReader(f)
                for line in csv_reader:
                    ITEMS.append(line)

            for i in range(len(ITEMS)):
                itemList = TwoLineListItem(text=ITEMS[i]["Item Name"], secondary_text = ITEMS[i]["Primary Unit"])
                self.card2layout.add_widget(itemList)
            self.itemsLabel.text = "ITEMS: " + str(i)

    def on_pre_enter(self):
        global itemListChanged
        if(itemListChanged):
            global ITEMS
            itemList = TwoLineListItem(text=ITEMS[len(ITEMS)-1]["Item Name"], secondary_text=ITEMS[len(ITEMS)-1]["Primary Unit"])
            self.card2layout.add_widget(itemList)
            self.itemsLabel.text = "ITEMS: " + str(len(ITEMS))

    def addItem(self):
        sm.current = "newitemscreen"
        sm.transition.direction = "left"





# ADD ITEM SCREEN
class NewItemScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mainlayout = MDBoxLayout(orientation='vertical')

        self.path_obj = folder_dialog_layout()

        self.save_sptax = ""
        self.save_pptax = ""
        self.save_itemName = ""
        self.save_batchNumber = ""
        self.save_unitMultiplier = ""
        self.save_primaryUnit = ""
        self.save_secondaryUnit = ""
        self.save_companyName = ""
        self.save_saleprice = ""
        self.save_sptaxInclusive = ""
        self.save_pptaxInclusive = ""
        self.save_expiryDate = ""
        self.save_dateAdded = ""
        self.save_openingStock = ""

        self.layout1 = MDBoxLayout(orientation='horizontal', spacing="10dp", padding="10dp")
        self.layout2 = MDBoxLayout(spacing="10dp", padding="10dp")
        self.layout3 = MDBoxLayout(spacing="10dp", padding="10dp")
        self.layout4 = MDBoxLayout(spacing="10dp", padding="10dp")
        self.layout5 = MDBoxLayout(spacing="10dp", padding="10dp")
        self.layout6 = MDBoxLayout(spacing="10dp", padding="10dp")


        self.itemName = Builder.load_string(itemNameHelper)
        self.batchNumber = Builder.load_string(batchNumberHelper)
        self.companyName = Builder.load_string(companyNameHelper)
        self.selectUnitBtn = MDRaisedButton(text="Select Unit *", size_hint_x=0.4, on_release = lambda x: self.showUnitDialog())
        self.salePrice = Builder.load_string(salePriceHelper)
        self.spInclusiveTaxLabel = MDLabel(text="Tax Inclusive", size_hint=(0.2,None),size=("40dp","40dp"))
        self.purchasePrice = Builder.load_string(purchasePriceHelper)
        self.ppInclusiveTaxLabel = MDLabel(text="Tax Inclusive", size_hint=(0.2,None),size=("40dp","40dp"))
        self.openingStock = Builder.load_string(openingStockHelper)
        self.addedDateCheckLabel = MDLabel(text="Added Date", size_hint=(0.1, None), size=("40dp","40dp"))
        self.addedDateCheck = MDCheckbox(size_hint=(0.2,None),size=("48dp","48dp"))
        self.addedDateCheck.bind(active= self.putAddedDate)
        self.addDate = False

        self.saveBtn = MDRaisedButton(text="Save", on_release= lambda x: self.Save())
        self.nextBtn = MDRaisedButton(text="Save and Next", on_release= lambda x: self.SaveAndNext())
        self.cancelBtn = MDRaisedButton(text="Cancel", on_release= lambda x: self.CancelItem())

        self.expiryDateBtn = MDRaisedButton(text="Add Expiry Date", on_release = lambda x: self.showExpiryDatePicker())
        self.expiryDateLabel = MDLabel(text="No Date Selected", size_hint=(0.4,None), size=("40dp","40dp"))

        self.sptaxButton = MDRaisedButton(text="Select Tax Amount", disabled=False, on_release = lambda x: self.showSPTax())
        self.pptaxButton = MDRaisedButton(text="Select Tax Amount", disabled=False, on_release = lambda x: self.showPPTax())


        self.spInclusiveCheckbox = MDCheckbox(size_hint=(0.2,None), size=("48dp","48dp"))
        self.spInclusiveCheckbox.bind(active= self.showSpTaxButton)
        self.spInclusiveTaxSelectLabel = MDLabel(text="Tax N/A",size_hint=(0.5,None),size=("40dp","40dp"))
        self.ppInclusiveCheckbox = MDCheckbox(size_hint=(0.2,None), size=("48dp","48dp"))
        self.ppInclusiveCheckbox.bind(active= self.showPpTaxButton)
        self.ppInclusiveTaxSelectLabel = MDLabel(text="Tax N/A",size_hint=(0.5,None),size=("40dp","40dp"))



        self.layout1.add_widget(self.itemName)
        self.layout1.add_widget(self.batchNumber)
        self.layout2.add_widget(self.companyName)
        self.layout2.add_widget(self.selectUnitBtn)
        self.layout3.add_widget(self.salePrice)
        self.layout3.add_widget(self.spInclusiveTaxLabel)
        self.layout3.add_widget(self.spInclusiveCheckbox)
        self.layout3.add_widget(self.sptaxButton)
        self.layout3.add_widget(self.spInclusiveTaxSelectLabel)
        self.layout4.add_widget(self.purchasePrice)
        self.layout4.add_widget(self.ppInclusiveTaxLabel)
        self.layout4.add_widget(self.ppInclusiveCheckbox)
        self.layout4.add_widget(self.pptaxButton)
        self.layout4.add_widget(self.ppInclusiveTaxSelectLabel)
        self.layout5.add_widget(self.openingStock)
        self.layout5.add_widget(self.expiryDateBtn)
        self.layout5.add_widget(self.expiryDateLabel)
        self.layout5.add_widget(self.addedDateCheckLabel)
        self.layout5.add_widget(self.addedDateCheck)
        self.layout6.add_widget(self.saveBtn)
        self.layout6.add_widget(self.nextBtn)
        self.layout6.add_widget(self.cancelBtn)

        mainlayout.add_widget(self.layout1)
        mainlayout.add_widget(self.layout2)
        mainlayout.add_widget(self.layout3)
        mainlayout.add_widget(self.layout4)
        mainlayout.add_widget(self.layout5)
        mainlayout.add_widget(self.layout6)

        self.add_widget(mainlayout)

# GET PRIMARY UNIT VALUE FROM DROPDOWN
    def getPrimaryUnit(self, instance_menu, pu):
        self.save_primaryUnit = pu.text

# GET SECONDARY UNIT VALUE FROM DROPDOWN
    def getSecondaryUnit(self, instance_menu, su):
        self.save_secondaryUnit = su.text

# SHOW SALES PRICE TAX DROPDOWN; FILL SPTAX DROPDOWN FROM TAX FILE
    def showSPTax(self):
        if(os.path.exists(MAINPATH + '/tax')):
            #sp_tax_dropdown = MDDropdownMenu(caller=self.sptaxButton, width_mult=4, position="bottom")
            #sp_tax_dropdown.bind(on_release = self.getSPTax)

            #with open(MAINPATH + '/tax', 'r') as f:
            #    lines = f.readlines()
            #    for line in lines:
            #        sp_tax_dropdown.items.append(
            #            { "viewclass": "MDMenuItem",
            #            "text": str(line.strip()),
                        #"height": "36dp",
                        #"top_pad": "10dp",
                        #"bot_pad": "10dp"
            #             }
            #        )
            #sp_tax_dropdown.open()

            sp_tax_dropdown = DropDown(auto_width=False, width = self.sptaxButton.width+5, effect_cls="ScrollEffect", scroll_type=['bars'])
            sp_tax_dropdown_gridlayout = MDGridLayout(cols=1, size_hint_y=None)
            sp_tax_dropdown.add_widget(sp_tax_dropdown_gridlayout)

            with open(MAINPATH + '/tax','r') as f:
                lines = f.readlines()
                for line in lines:
                    btn = MDRaisedButton(text=line.strip(),on_release=self.getSPTax, increment_width=sp_tax_dropdown.width-60)
                    sp_tax_dropdown_gridlayout.add_widget(btn)
            sp_tax_dropdown.open(self.sptaxButton)

        else:
            with open(MAINPATH + '/tax', 'w') as f:
                for i in taxlist:
                    f.write(i + "\n")

# FETCH SALES PRICE TAX AMOUNT FROM SPTAX TEXTFIELD
    def getSPTax(self, sptax):
        self.save_sptax = sptax.text
        self.spInclusiveTaxSelectLabel.text = self.save_sptax

# SHOW PURCHASE PRICE TAX DROPDOWN; FILL DROPDOWN FROM TAX FILE
    def showPPTax(self):
        #if(os.path.exists(MAINPATH + '/tax')):
        #    pp_tax_dropdown = MDDropdownMenu(caller=self.sptaxButton, width_mult=4, position="bottom")
        #    pp_tax_dropdown.bind(on_release = self.getPPTax)
#
 #           with open(MAINPATH + '/tax', 'r') as f:
 #               lines = f.readlines()
 #               for line in lines:
 #                   pp_tax_dropdown.items.append(
 #                       { "viewclass": "MDMenuItem",
 #                       "text": str(line.strip())
                        #"height": "36dp",
                        #"top_pad": "10dp",
                        #"bot_pad": "10dp"
 #                       }
 #                   )
            #pp_tax_dropdown.open()
        if(os.path.exists(MAINPATH + '/tax')):
            pp_tax_dropdown = DropDown(auto_width=False, width = self.pptaxButton.width+5)
            with open(MAINPATH + '/tax','r') as f:
                lines = f.readlines()
                for line in lines:
                    btn = MDRaisedButton(text=line.strip(),on_release=self.getPPTax, increment_width=pp_tax_dropdown.width-60)
                    pp_tax_dropdown.add_widget(btn)
            pp_tax_dropdown.open(self.pptaxButton)
        else:
            with open(MAINPATH + '/tax', 'w') as f:
                for i in taxlist:
                    f.write(i + "\n")

    def getPPTax(self, pptax):
        self.save_pptax = pptax.text
        self.ppInclusiveTaxSelectLabel.text = self.save_pptax

# DISPLAYING UNIT SELECTION DIALOG
    def showUnitDialog(self):
        self.unitdialog = MDDialog(text="Select Unit", type="custom", content_cls=unit_dialog_layout(),height="200dp",auto_dismiss=False,
        buttons=[
            MDRaisedButton(text="Ok", on_release = lambda x: self.get_units()),
            MDFlatButton(text="Cancel", on_release = lambda x: self.close_unit_dialog(1))
        ])
        self.unitdialog.open()

# GETTING PRIMARY, SECONDARY AND MULTIPLIER FROM UNIT DIALOG
    def get_units(self):
        global unitMultiplierSelected
        global primaryUnitSelected
        global secondaryUnitSelected
        self.save_unitMultiplier = unitMultiplierSelected
        self.itemName.helper_text = str( " 1 " + primaryUnitSelected + " = " + unitMultiplierSelected + secondaryUnitSelected)
        self.itemName.helper_text_mode = "persistent"
        self.unitdialog.dismiss()


# CLOSE UNIT DIALOG
    def close_unit_dialog(self, value):
        if value:
            self.unitdialog.dismiss()

# SHOW EXPIRY DATE PICKER
    def showExpiryDatePicker(self):
        picker = MDDatePicker(callback=self.get_date)
        picker.open()

# ENABLE SALE PRICE BUTTON ON CHECKBOX CHECK
    def showSpTaxButton(self, checkbox, value):
        if value:
            self.sptaxButton.disabled = True
            self.spInclusiveTaxSelectLabel.text = "Tax N/A"
            self.save_sptaxInclusive = "Yes"
        else:
            self.sptaxButton.disabled = False
            self.save_sptaxInclusive = "No"

# ENABLE PURCHASE PRICE BUTTON ON CHECKBOX CHECK
    def showPpTaxButton(self, checkbox, value):
        if value:
            self.pptaxButton.disabled = True
            self.ppInclusiveTaxSelectLabel.text = "Tax N/A"
            self.save_pptaxInclusive = "Yes"
        else:
            self.pptaxButton.disabled = False
            self.save_pptaxInclusive = "No"

# GET EXPIRY DATE
    def get_date(self, date):
        self.expiryDateLabel.text = "Expiry Date: " + str(date)
        self.save_expiryDate = str(date.day) + "/" + str(date.month) + "/" + str(date.year)

# ADD ADDED DATE OR NOT
    def putAddedDate(self, checkbox, value):
        if value:
            self.addDate = True
        else:
            self.addDate = False

# SAVING NEW ITEM DETAILS
    def Save(self):
        global primaryUnitSelected
        global secondaryUnitSelected
        global ItemScreenCalled

        self.save_itemName = self.itemName.text
        self.save_companyName = self.companyName.text
        self.save_saleprice = self.salePrice.text
        today = date.today()
        self.save_dateAdded = today.strftime("%d/%m/%y")
        self.save_openingStock = self.openingStock.text
        self.save_batchNumber = self.batchNumber.text
        self.save_primaryUnit = primaryUnitSelected
        self.save_secondaryUnit = secondaryUnitSelected

        if(self.save_itemName != "" and self.save_companyName != "" and self.save_primaryUnit != "" and self.save_secondaryUnit != ""):
                if(os.path.exists(MAINPATH + '/items')):
                    item_fields = ["Item Name", "Batch Number", "Primary Unit", "Unit Multiplier","Secondary Unit",
                    "Sale Price", "SP Tax Inclusive", "SP Tax", "Purchase Price", "PP Tax Inclusive", "PP Tax", "Company",
                    "Expiry Date", "Opening Stock", "Date Added"]
                    global ITEMS
                    with open(MAINPATH + '/items', 'a+') as f:
                        csv_reader = csv.DictWriter(f, fieldnames=item_fields)
                        if(self.addDate):
                            itemWrite = {"Item Name" : self.save_itemName, "Batch Number" : self.save_batchNumber, "Primary Unit" : self.save_primaryUnit,
                                "Unit Multiplier" : self.save_unitMultiplier, "Secondary Unit" : self.save_secondaryUnit, "Sale Price" : self.save_saleprice,
                                "SP Tax Inclusive" : self.save_sptaxInclusive, "SP Tax" : self.save_sptax, "Purchase Price" : self.purchasePrice.text,
                                "PP Tax Inclusive" : self.save_pptaxInclusive, "PP Tax" : self.save_pptax, "Company" : self.companyName.text,
                                         "Expiry Date" : self.save_expiryDate, "Opening Stock" : self.save_openingStock, "Date Added" : self.save_dateAdded}

                            csv_reader.writerow(itemWrite)
                            ITEMS.append(itemWrite)
                        else:
                            itemWrite = {"Item Name" : self.save_itemName, "Batch Number" : self.save_batchNumber, "Primary Unit" : self.save_primaryUnit,
                                "Unit Multiplier" : self.save_unitMultiplier, "Secondary Unit" : self.save_secondaryUnit, "Sale Price" : self.save_saleprice,
                                "SP Tax Inclusive" : self.save_sptaxInclusive, "SP Tax" : self.save_sptax, "Purchase Price" : self.purchasePrice.text,
                                "PP Tax Inclusive" : self.save_pptaxInclusive, "PP Tax" : self.save_pptax, "Company" : self.companyName.text,
                                "Expiry Date" : self.save_expiryDate, "Opening Stock" : self.save_openingStock}

                            csv_reader.writerow(itemWrite)
                            ITEMS.append(itemWrite)

                    global itemListChanged
                    self.ResetItem()
                    itemListChanged = True
                    sm.current = "itemscreen"
                    sm.transition.direction = "right"


                    #Snackbar(text="Item Added! Please Wait", padding="0dp").open()
                    n.update("Item Added Succesfully!","")
                    n.show()

                else:
                    if(MAINPATH != ""):
                        with open(MAINPATH + '/items', 'w') as f:
                            f.write("Item Name,Batch Number,Primary Unit,Unit Multiplier,Secondary Unit,Sale Price,SP Tax Inclusive,SP Tax,Purchase Price,PP Tax Inclusive,PP Tax,Company,Expiry Date,Opening Stock,Date Added,Days Remaining\n")
        else:
            #Snackbar(text="Please fill the required details before proceeding!", padding="0dp", font_size="14sp").open()
            n.update("Please fill the required details","")
            n.show()

    def SaveAndNext(self):
        pass

    def ResetItem(self):
        self.itemName.text = ""
        self.itemName.helper_text = ""
        self.itemName.helper_text_mode = "on_focus"
        self.batchNumber.text = ""
        self.companyName.text = ""
        self.salePrice.text = ""
        self.purchasePrice.text = ""
        self.openingStock.text = ""
        self.expiryDateLabel.text = "No Date Selected"
        unit_dialog_layout().primaryUnitLabel.text = ""
        unit_dialog_layout().secondaryUnitLabel.text = ""
        unit_dialog_layout().unitMultiplier.text = ""
        self.spInclusiveCheckbox.active = False
        self.ppInclusiveCheckbox.active = False
        self.spInclusiveTaxSelectLabel.text = "Tax N/A"
        self.ppInclusiveTaxSelectLabel.text = "Tax N/A"
        self.addedDateCheck.active = False

    def CancelItem(self):
        self.ResetItem()
        sm.current = "itemscreen"
        sm.transition.direction = "right"


# HISTORY SCREEN
class HistoryScreen(Screen):
    pass

# HOME SCREEN
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDGridLayout(cols=2,spacing="10dp",padding="10dp")
        for i in range(6):
            card = MDCard()
            cardlayout = MDBoxLayout()
            cardlabel = MDLabel(text=str(i))
            cardlayout.add_widget(cardlabel)
            card.add_widget(cardlayout)
            layout.add_widget(card)
        self.add_widget(layout)

# PURCHASE SCREEN
class PurchaseScreen(Screen):
    pass

# SETTING SCREEN
class SettingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# PARTIES SCREEN
class PartyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDGridLayout(cols=2,padding="5dp",spacing="5dp")
        leftbar = MDGridLayout(rows=2,cols=1,spacing="6dp",size_hint_x=0.4)

        card1 = MDCard(size_hint_y=0.19,elevation=3)
        card2 = MDCard(elevation=3)
        card3 = MDCard(elevation=0)

        card1layout = MDGridLayout(rows=4,padding="2dp",spacing="2dp")
        card1innerlayout = MDBoxLayout(spacing="2dp", padding="2dp")

        self.partiesLabel = MDLabel(text="", size_hint=(1,None), size=("40dp","40dp"),font_style="H5")
        sortBtn = MDIconButton(icon="filter", size_hint=(None,None),size=("20dp","20dp"))
        searchBtn = MDIconButton(icon="android",size_hint=(None,None), size=("20dp","20dp"))
        partyBtn = MDRaisedButton(text="+ PARTY", on_release= lambda x: self.addParty())


        card1innerlayout.add_widget(self.partiesLabel)
        card1innerlayout.add_widget(sortBtn)
        card1innerlayout.add_widget(searchBtn)

        card1layout.add_widget(card1innerlayout)
        card1layout.add_widget(partyBtn)


        self.card2layoutPartyScrollView = ScrollView(bar_width=4, bar_inactive_color=[.7,.7,.7,.5])
        
        self.card2layoutParty = MDGridLayout(cols=1, size_hint_y=None)
        self.card2layoutParty.bind(minimum_height=self.card2layoutParty.setter('height'))

        self.card2layoutPartyScrollView.add_widget(self.card2layoutParty)

        card3layout = MDGridLayout()

        card1.add_widget(card1layout)
        card2.add_widget(self.card2layoutPartyScrollView)
        card3.add_widget(card3layout)

        leftbar.add_widget(card1)
        leftbar.add_widget(card2)


        layout.add_widget(leftbar)
        layout.add_widget(card3)
        self.add_widget(layout)

        global PARTIES

        if(os.path.exists(MAINPATH + '/parties')):
            with open(MAINPATH + '/parties', 'r') as f:
                csv_reader = csv.DictReader(f)
                for line in csv_reader:
                    PARTIES.append(line)
            
            for i in range(len(PARTIES)):
                partyList = TwoLineListItem(text=PARTIES[i]["Party Name"], secondary_text = PARTIES[i]["Party Code"])
                self.card2layoutParty.add_widget(partyList)
            self.partiesLabel.text = "PARTIES: " + str(i)
    
    def on_pre_enter(self):
        global partyListChanged
        if(partyListChanged):
            global PARTIES
            partyList = TwoLineListItem(text=PARTIES[len(PARTIES)-1]["Party Name"], secondary_text=PARTIES[len(PARTIES)-1]["Party Code"])
            self.card2layoutParty.add_widget(partyList)
            self.partiesLabel.text = "PARTIES: " + str(len(PARTIES))

    def addParty(self):
        sm.current = "newpartyscreen"
        sm.transition.direction = "left"

partyNameHelper = """
MDTextField:
    hint_text: "Name *"
    write_tab: False
    multiline: False
"""
partyCodeHelper = """
MDTextField:
    hint_text: "Code"
    write_tab: False
    multiline: False
"""
partyPhoneHelper = """
MDTextField:
    hint_text: "Phone"
    write_tab: False
    multiline: False
"""
partyAddressHelper = """
MDTextField:
    hint_text: "Address *"
    write_tab: False
    multiline: True
"""
partyPincodeHelper = """
MDTextField:
    hint_text: "Pincode"
    write_tab: False
    multiline: True
"""
# NEW PARTY ADDITION SCREEN
class NewPartyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mainlayout = MDBoxLayout(orientation='vertical', spacing="10dp", padding="10dp")

        layout1 = MDBoxLayout(spacing="10dp", padding="10dp")
        layout2 = MDBoxLayout(spacing="10dp", padding="10dp")
        layout3 = MDBoxLayout(spacing="10dp", padding="10dp")
        layout4 = MDBoxLayout(spacing="10dp", padding="10dp")

        self.partyName = Builder.load_string(partyNameHelper)
        self.partyCode = Builder.load_string(partyCodeHelper)
        self.partyPhone = Builder.load_string(partyPhoneHelper)
        self.partyAddress = Builder.load_string(partyAddressHelper)
        self.partyPincode = Builder.load_string(partyPincodeHelper)
        self.partySaveBtn = MDRaisedButton(text= "Save", on_release=lambda x: self.SaveParty())
        self.partySaveNextBtn = MDRaisedButton(text="Save and Next", on_release=lambda x: self.SaveNextParty())
        self.partyCancelBtn = MDRaisedButton(text="Cancel", on_release=lambda x:self.CancelParty())

        layout1.add_widget(self.partyName)
        layout2.add_widget(self.partyCode)
        layout2.add_widget(self.partyPhone)
        layout3.add_widget(self.partyAddress)
        layout3.add_widget(self.partyPincode)
        layout4.add_widget(self.partySaveBtn)
        layout4.add_widget(self.partySaveNextBtn)
        layout4.add_widget(self.partyCancelBtn)

        mainlayout.add_widget(layout1)
        mainlayout.add_widget(layout2)
        mainlayout.add_widget(layout3)
        mainlayout.add_widget(layout4)


        self.add_widget(mainlayout)

    def SaveParty(self):
        global partyListChanged
        if(self.partyName.text != "" and self.partyPhone.text != ""):
            if(os.path.exists(MAINPATH + '/parties')):
                fieldnames = ["Party Name","Party Code","Party Phone","Party Address","Party Pincode"]
                partyWrite = {"Party Name" : self.partyName.text, "Party Code" : self.partyCode.text, "Party Phone" : self.partyPhone.text, "Party Address" : self.partyAddress.text,
                              "Party Pincode" : self.partyPincode.text}
                with open(MAINPATH + '/parties','a+') as f:
                    csv_reader = csv.DictWriter(f, fieldnames=fieldnames)
                    csv_reader.writerow(partyWrite)
                    #f.write(
                    #    self.partyName.text + "," + self.partyCode.text + "," + self.partyPhone.text + "," + self.partyAddress.text + ","
                    #    + self.partyPincode.text
                    #)
                partyListChanged = True
                global PARTIES
                PARTIES.append(partyWrite)
                sm.current = "partyscreen"
                sm.transition.direction = "right"

            else:
                with open(MAINPATH + '/parties','w') as f:
                    f.write("Party Name,Party Code,Party Phone,Party Address,Party Pincode\n")
        else:
            n.update("Please fill the details before proceeding!","")
            n.show()

    def SaveNextParty(self):
        pass

    def CancelParty(self):
        sm.current = "partyscreen"
        sm.transition.direction = "right"
        self.partyName.text = ""
        self.partyCode.text = ""
        self.partyAddress.text = ""
        self.partyPhone.text = ""
        self.partyPincode.text = ""




# INVENTORY SCREEN
#class InventoryScreen(Screen):
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#    def on_pre_enter(self):
#        layout = FloatLayout()
#        FILTER_ITEMS = ["Sale Price", "SP Tax Inclusive", "SP Tax", "Purchase Price", "PP Tax Inclusive","PP Tax", "Date Added"]
#
#        col_dat = [
#            ("No.",dp(10)),
#            ("Item", dp(40)),
#            ("BAT No.", dp(30)),
#            ("PR Unit", dp(30)),
#            ("Unit", dp(30)),
#            ("SEC Unit", dp(30)),
            #("Sale Price", dp(30)),
            #("SP Tax Inclusive", dp(30)),
            #("SP Tax", dp(30)),
            #("Purchase Price", dp(30)),
            #("PP Tax Inclusive", dp(30)),
            #("PP Tax", dp(30)),
#            ("Co.", dp(30)),
#            ("Exp Date", dp(20)),
#            ("Stock", dp(20)),
#            ("D. Remaining", dp(20)),
            #("Date Added", dp(30)),
#             ]
#        row_dat = []
#        row_dat_tup = []
#        exp = False
#        for i in range(len(ITEMS)):
#            for k,v in ITEMS[i].items():
#                if(k not in FILTER_ITEMS):
#                    if(v != "" and k != "Expiry Date"):
#                        row_dat_tup.append(v)
#                    elif(k == "Expiry Date"):
#                        EXP = v.split("/")
#                        row_dat_tup.append(v)
#                        exp = True
#                    else:
#                        row_dat_tup.append("-")
#            
#            row_dat_tup.insert(0,i+1)
#            if(exp):
#                D_REM = date(int(EXP[2]),int(EXP[1]),int(EXP[0])) - date.today()
#                row_dat_tup[len(row_dat_tup)-1] = D_REM.days
#
#                exp = False
#            else:
#                row_dat_tup[len(row_dat_tup)-1] = "-"
#
#            row_dat_tup = tuple(row_dat_tup)
#            row_dat.append(row_dat_tup)
#            row_dat_tup = []
#
#        dt = MDDataTable(column_data=col_dat, row_data=row_dat, use_pagination=True, sort=True)
#        layout.add_widget(dt)
#        self.add_widget(layout)


class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ITEM_CONTAINER = []
        self.IS_TABLE_SORTED = False

    def on_pre_enter(self):
        self.spinner = MDSpinner(size_hint=(None,None),size=("46dp","46dp"), pos_hint={"center_x":.5,"center_y":.5})
        self.add_widget(self.spinner)

    def on_enter(self):
        global ITEMS
        self.show_table(ITEMS)

    def show_table(self, arr):
        FILTER_ITEMS = ["Sale Price", "SP Tax Inclusive", "SP Tax", "Purchase Price", "PP Tax Inclusive","PP Tax", "Date Added"]

        col_dat = [
            ("No.", dp(8)),
            ("Item", dp(30)),
            ("BAT No.", dp(20)),
            ("P. Unit", dp(8)),
            ("Unit", dp(8)),
            ("S. Unit", dp(8)),
            ("Co.", dp(20)),
            ("Exp Date", dp(20)),
            ("Stock", dp(20)),
            ("Days Rem", dp(10))
            ]
        self.layout = MDGridLayout(cols=len(col_dat), padding="10dp")

        for i in col_dat:
            btn = TableButton(text=i[0], background_color=[0.1,0.6,0.9,1], size_hint_y=None, height="60dp", on_release = self.SortTable)
            self.layout.add_widget(btn)

        exp = False
        alternate = False
        row_dat = []
        for i in range(len(arr)):
            for k,v in arr[i].items():
                if(k not in FILTER_ITEMS):
                    if(v != "" and k != "Expiry Date"):
                        row_dat.append(v)
                    elif(k == "Expiry Date" and v != ""):
                        EXP = v.split("/")
                        row_dat.append(v)
                        exp = True
                    else:
                        row_dat.append("N/A")
            row_dat.insert(0,i+1)
            if(exp):
                D_REM = date(int(EXP[2]),int(EXP[1]),int(EXP[0])) - date.today()
                row_dat[len(row_dat)-1] = str(D_REM.days)+"\dr"
                arr[i]["Days Remaining"] = D_REM.days
                exp = False
            else:
                row_dat[len(row_dat)-1] = "N/A\dr"
                arr[i]["Days Remaining"] = inf

            for i in range(len(row_dat)):
                if(alternate):
                    if("\dr" in str(row_dat[i])):
                        row_dat[i] = row_dat[i].strip("\dr")
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.2], color=[1,0,0,1], size_hint_y=None, height="50dp", font_size="18sp", size_hint_x=col_dat[i][1])
                        alternate = False
                    elif("N/A\dr" in str(row_dat[i])):
                        row_dat[i] = row_dat[i].strip("\dr")
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.2], color=[0,0,0,1], size_hint_y=None, height="50dp", font_size="18sp", size_hint_x=col_dat[i][1])
                        alternate = False
                    else:
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.2], color=[0,0,0,1], size_hint_y=None, height="50dp", size_hint_x=col_dat[i][1])
                    self.layout.add_widget(btn)
                else:
                    if("\dr" in str(row_dat[i])):
                        row_dat[i] = row_dat[i].strip("\dr")
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.1], color=[1,0,0,1], size_hint_y=None, height="50dp", font_size="18sp", size_hint_x=col_dat[i][1])
                        alternate = True
                    elif("N/A\dr" in str(row_dat[i])):
                        row_dat[i] = row_dat[i].strip("\dr")
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.2], color=[0,0,0,1], size_hint_y=None, height="50dp", font_size="18sp", size_hint_x=col_dat[i][1])
                        alternate = True

                    else:
                        btn = TableButton(text=str(row_dat[i]), background_color=[1,1,1,0.1], color=[0,0,0,1], size_hint_y=None, height="50dp", size_hint_x=col_dat[i][1])
                    self.layout.add_widget(btn)
            row_dat = []
        print(ITEMS)
        self.add_widget(self.layout)
        self.spinner.active = False
        self.remove_widget(self.spinner)

    def on_pre_leave(self):
        self.remove_widget(self.layout)

    def SortTable(self, instance):
        global ITEMS
        SORT_BY = instance.text
        self.remove_widget(self.layout)
        self.spinner = MDSpinner(size_hint=(None,None),size=("46dp","46dp"))
        self.spinner.active = True
        if(SORT_BY == "Item"):
            SORT_BY = "Item Name"
        elif(SORT_BY == "BAT No."):
            SORT_BY = "Batch Number"
        elif(SORT_BY == "P. Unit"):
            SORT_BY = "Primary Unit"
        elif(SORT_BY == "Unit"):
            SORT_BY = "Unit Multiplier"
        elif(SORT_BY == "S. Unit"):
            SORT_BY = "Secondary Unit"
        elif(SORT_BY == "Co."):
            SORT_BY = "Company"
        elif(SORT_BY == "Exp Date"):
            SORT_BY = "Days Remaining"
        elif(SORT_BY == "Stock"):
            SORT_BY = "Opening Stock"
        elif(SORT_BY == "Days Rem"):
            SORT_BY = "Days Remaining"
        else:
            pass

        if(self.IS_TABLE_SORTED == False):
            SORTED_ITEMS = sorted(ITEMS, key= lambda i: i[SORT_BY])
            self.IS_TABLE_SORTED = True
        else:
            SORTED_ITEMS = sorted(ITEMS, key= lambda i: i[SORT_BY], reverse = True)
            self.IS_TABLE_SORTED = False
        self.show_table(SORTED_ITEMS)


# ASK FOR EXIT CONFIRMATION WHEN USER EXITS LAYOUT

exitCounter = 0

class DCash(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if(os.path.isfile(logName)):
            global MAINPATH
            with open(logName,'r') as f:
                MAINPATH = f.read()
        else:
            self.folder_dialog = MDDialog(title="Select Folder", type="custom", content_cls=folder_dialog_layout())
            self.folder_dialog.open()

    def build(self):
        Window.minimum_height = 700
        Window.minimum_width = 1200
        Window.bind(on_request_close= lambda x: self.ask_on_exit(1))
        #self.theme_cls.primary_palette = "Green"
        #self.theme_cls.theme_style = "Light"
        return Main()


    def closeSaveDialog(self):
        self.sure_dialog = MDDialog(text="Are you sure?", buttons=[
            MDRaisedButton(text="Yes", on_release = lambda x: self.suredialogclose(0)),
            MDRaisedButton(text="No", on_release = lambda x: self.suredialogclose(1))
        ])
        self.sure_dialog.open()

    def suredialogclose(self, value):
        global mainFolder
        global logName
        global folderName

        path = mainFolder
        if value:
            self.sure_dialog.dismiss()
        else:
            self.sure_dialog.dismiss()
            #self.folder_dialog.dismiss()
            try:
                os.mkdir(path + '/' + folderName)
            except FileExistsError:
                shutil.rmtree(path + '/' + folderName)
                os.mkdir(path + '/' + folderName)
            with open(logName, 'w') as f:
                f.write(path + '/' + folderName)

    def ask_on_exit(self, counter):
        global exitCounter
        exitCounter = exitCounter + counter
        if(exitCounter == 1):
            self.exit_dialog = MDDialog(auto_dismiss=False, text="Are you sure?",
                                        buttons=[
                                            MDFlatButton(text="Yes",text_color=self.theme_cls.primary_color, on_release = lambda x: self.exit_app(1)),
                                            MDFlatButton(text="No", text_color=self.theme_cls.primary_color, on_release = lambda x: self.exit_app(0))])
            self.exit_dialog.open()
        return True
    
    def exit_app(self, value):
        global exitCounter
        if value:
            exit(0)
        else:
            self.exit_dialog.dismiss()
            exitCounter = 0

    def close_on_exit_popup(self):
        self.popup.dismiss()
        self.stop

if __name__ == "__main__":
    DCash().run()
