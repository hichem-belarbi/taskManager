from PyQt5.QtWidgets import QDialog,QWidget,QVBoxLayout,QGraphicsDropShadowEffect,QApplication,QMainWindow,QMenu,QAction,QToolButton,QLabel,QPushButton
from PyQt5.uic import loadUi
import sys,os
from PyQt5.QtGui import QColor,QIcon,QPixmap
from PyQt5.QtCore import QTimer,Qt
import random
from myAnimation import myAnimation
from datetime import datetime,date
from matplotlib.figure import Figure
from numpy import arange

##########################################################
#des fonctions communes 
#########################################################
#fonction pour animer la wiget de notifications
def lever_une_notif(message="",duration=2000):
    fenetre.notif_widget.show()
    def cacher():
        notif_animation.D_Move(200,1)
  
    fenetre.message_notif_widget.setText(message)
    notif_animation.U_Move(200,1)

    QTimer.singleShot(duration,cacher)
    pass   
    
#tester si les fichier des données existe et les creer si non 
#et lever une notification
def verifier_lexistance_des_fichier():
    if not os.path.isfile("liste_des_taches.txt"):
        fenetre.alertdepertedestachesstockees.setText("les taches mémorisées la dernière fois sont perdues !")
        with open ("liste_des_taches.txt","w") as fp:
            pass
    if not os .path.isfile("statistiques_des_taches.txt"):
        
        with open ("statistiques_des_taches.txt","w") as fp:
            fp.write("0_0_0_0")
    
#Cette fonction change la couleur de l'ambre derriere les widgets 
def petite_ambiance():
    rgb=random.choice([(62,117,148),(60,158,126),(125,38,37),(187,160,15),(104,158,174)])
    if not(fenetre.led.isChecked()):
        rgb=(0,0,0)
        Q.stop()
    for widget in widgetlist:  
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(rgb[0],rgb[1],rgb[2]))  
        shadow.setOffset(0,0)
        widget.setGraphicsEffect(shadow)
#¸affichage du menu lateral
def hide_show_sidemenu():
    if fenetre.opensidemenubutton.isChecked():
        sidemenu_animation.increase_width(200,1)
    else:
        sidemenu_animation.increase_width(-200,1)
    fenetre.opensidemenubutton.setEnabled(False)
    QTimer.singleShot(500,lambda:fenetre.opensidemenubutton.setEnabled(True))
###########################################"
###########################################
#########################################       




#########################################################,,,,,
#des fonctionq qui gerent la page d'acceuille                   >>>
##########################################################''''
def home_page():
    def update(labels,statics,labelsglobal,statisticsglobal):
        ax.clear()
        ax_global.clear()
        
        #perso des axes :
        for tickx in ax.xaxis.get_ticklabels():
            tickx.set_color("white")   
        for ticky in ax.yaxis.get_ticklabels():
            ticky.set_color("white")
            
        for tickx in ax_global.xaxis.get_ticklabels():
            tickx.set_color("white")
            
        for ticky in ax_global.yaxis.get_ticklabels():
            ticky.set_color("white")

        ax.set_yticks([0]*statics[0])
        ax_global.set_yticks([0]*statisticsglobal[0])
        ax.set_title("ACTUEL",color="white")
        ax_global.set_title("HISTORIQUE",color="white")
        #############################  
        pg=ax_global.bar(labelsglobal,statisticsglobal,color=(152/255,31/255,31/255))   
        p=ax.bar(labels,statics,color=(152/255,31/255,31/255))
        ax.bar_label(p, label_type='edge',color="white")
        ax_global.bar_label(pg, label_type='edge',color="white")
        fig.tight_layout()
        fig.savefig("graphe.png")
        pixmap=QPixmap("graphe.png")
        fenetre.graphe_acc_label.setPixmap(pixmap)
        os.remove("graphe.png")


    #fonction pour afficher la dialog d'ajout une tache:
    def ajouter_une_tache():
        if not fenetre.change_permission_button.isChecked():
            dialog_dajout.titre.setText("")
            dialog_dajout.objectif.setText("")
            dialog_dajout.date.setDate(date(1753,1,1))
            dialog_dajout.importanceslider.setValue(0)
            dialog_dajout.show()
           
    #pour effacer une tache  definitivement
    def effacer_une_tache(index):
        label=list_des_labels[index-(len(list_des_widget_des_taches)-len(list_des_labels))]
        if label!=[]:
            label.hide()
            fait_ou_non=list_des_widget_des_taches[index][4]
        else:
            list_des_widget_des_taches[index].close()
            fait_ou_non=list_des_widget_des_taches[index].faitounon.text()
        dialog_de_confirmation.close()
        
        #verifier si le widget est new ou non pour resoudre le probleme
        #de la suppression d'une tache new
        #decrimenter les statistiques
        if fait_ou_non=="pas Fait\n":
            statics[2]-=1
            fenetre.pasfait_num_label.setText(f"PAS FAIT:\n{statics[2]}")
        else:
            statics[1]-=1
            fenetre.fait_num_label.setText(f"FAIT:\n{statics[1]}")
        statics[0]-=1
        fenetre.total_num_label.setText(f"TOTAL:\n{statics[0]}")
        statistics_global[3]+=1
        dialog_de_confirmation.oui.disconnect()
        del list_des_widget_des_taches[index] 
        
        
        update(labels,statics,labels_golbal,statistics_global)
        
    #demander_la_confirmation_pour_la_suppression si on click sur le bouton de suppression d'une tache
    def demander_la_confirmation_pour_la_suppression(index):
        if not fenetre.change_permission_button.isChecked():
            dialog_de_confirmation.show()
            dialog_de_confirmation.oui.clicked.connect(lambda check,index=index:effacer_une_tache(index))
        

    
    #pour marker une tache comme fait ou pas fait
    def tager_fait_ou_non(check,widget_de_tache,initialisation=False):
        if not fenetre.change_permission_button.isChecked():

            if check:
                #icrementer le nombre des tache faites et  l'inverse 
                statics[1]+=1
                fenetre.fait_num_label.setText(f"FAIT:\n{statics[1]}")
                
                if not initialisation:
                    
                    statics[2]-=1
                    fenetre.pasfait_num_label.setText(f"PAS FAIT:\n{statics[2]}")
                    statistics_global[1]+=1
                    statistics_global[2]-=1
                #####
                widget_de_tache.faitounon.setText("Fait\n")
                widget_de_tache.fait_button.setText("pas Fait")
                widget_de_tache.fait_button.setChecked(True)
                widget_de_tache.faitounontag.setIcon(QIcon("bookmark (1).png"))
            else:
                #icrementer le nombre des taches pas faites et l'inverse
                statics[2]+=1
                fenetre.pasfait_num_label.setText(f"PAS FAIT:\n{statics[2]}")
                
                if not initialisation:
                    statistics_global[2]+=1
                    statistics_global[1]-=1
                    statics[1]-=1
                    fenetre.fait_num_label.setText(f"FAIT:\n{statics[1]}")
                #####

                widget_de_tache.faitounon.setText("pas Fait\n")
                widget_de_tache.fait_button.setText("Fait")
                widget_de_tache.fait_button.setChecked(False)
                widget_de_tache.faitounontag.setIcon(QIcon("bookmark.png")) 
            if not initialisation:
                update(labels,statics,labels_golbal,statistics_global)
                
    def transformer_en_label(event,valeurs,widget_de_tache,ordre)  :
                    valeurs[4]=widget_de_tache.faitounon.text()     
                    titre=valeurs[0]
                    date=valeurs[2]
                    index=list_des_widget_des_taches.index(widget_de_tache) 
                    list_des_widget_des_taches[index]=valeurs 
                    contenu=f'{ordre+1}) Titre: {titre}{" "*(20-len(titre))}|\n               {date}'
                    label=QPushButton()

                    label.setStyleSheet('''QPushButton{text-align:center;background:rgb(50,50,50);border-radius:10px;color:white;font: 14pt "Consolas";border:1px solid rgb(152,32,32)}QPushButton:hover{border:1px solid rgb(255,255,255);}''')
                    shadow = QGraphicsDropShadowEffect()   
                    shadow.setBlurRadius(10)   
                    shadow.setColor(QColor(0,0,0))  
                    shadow.setOffset(0,0)  
                    label.setGraphicsEffect(shadow)   
                    label.setFixedHeight(80)    
                    label.setText(contenu)   
                    label.enterEvent=lambda event,label=label:add_arrow(event,label)
                    label.leaveEvent=lambda event,label=label:remove_arrow(event,label)
                    layout_des_taches.addWidget(label)
                    list_des_widget_des_taches[ordre]=valeurs
                    label.clicked.connect(lambda event,valeurs=valeurs,label=label,ordre=ordre:transformer_en_widget(event,valeurs,label,ordre))   
                    layout_des_taches.replaceWidget(widget_de_tache,label)
                    list_des_labels[list_des_labels.index("000")]=label 
                    widget_de_tache.deleteLater()          
                
    def transformer_en_widget(event,valeurs,label,ordre):
                    list_des_labels[list_des_labels.index(label)]="000"
                    titre=valeurs[0]
                    objectif=valeurs[1]
                    date=valeurs[2]
                    importance=valeurs[3]
                    fait_ou_non=valeurs[4]
                    widget_de_tache=QWidget()
                    loadUi("taskwidget.ui",widget_de_tache)
                    widget_de_tache.setFixedHeight(156)


                    # faire un effet d'ambre pour les souswidget de la widget de tache 
                    listy=[widget_de_tache,widget_de_tache.objectif,widget_de_tache.date,widget_de_tache.fait_button,widget_de_tache.clear,widget_de_tache.faitounontag,widget_de_tache.title]
                    for component in listy:
                        shadow = QGraphicsDropShadowEffect()
                        shadow.setBlurRadius(10)
                        shadow.setColor(QColor(0,0,0))  
                        shadow.setOffset(0,0)
                        component.setGraphicsEffect(shadow)

                    #afficter les valeur
                    widget_de_tache.importancelabel.setText(str(importance)+"%")
                    widget_de_tache.faitounon.setText(fait_ou_non)
                    widget_de_tache.title.setText(titre)
                    if date=="":
                        date="--/--/----"
                    
                    widget_de_tache.date.setText(date)
                    widget_de_tache.objectif.setText(objectif.replace("#","\n"))
                    index=list_des_widget_des_taches.index(valeurs)
                    widget_de_tache.ordre_ou_nouveau.setText(str(ordre+1))
                    
                    #########
                    #ajouter la widget a la liste des widget des tache
                    list_des_widget_des_taches[index]=widget_de_tache
                    #regler le bouton "clear" pour efaccer la tache correspendante
                    widget_de_tache.clear.clicked.connect(lambda check,index=index:demander_la_confirmation_pour_la_suppression(index))
                    #tester si on va tager comme fait ou non :
                    if fait_ou_non=="Fait\n":
                        widget_de_tache.faitounon.setText("Fait\n")
                        widget_de_tache.fait_button.setText("pas Fait")
                        widget_de_tache.fait_button.setChecked(True)
                        widget_de_tache.faitounontag.setIcon(QIcon("bookmark (1).png"))
                    else:
                        widget_de_tache.faitounon.setText("pas Fait\n")
                        widget_de_tache.fait_button.setText("Fait")
                        widget_de_tache.fait_button.setChecked(False)
                        widget_de_tache.faitounontag.setIcon(QIcon("bookmark.png")) 

                    #pour tager une tache comme fait
                    widget_de_tache.fait_button.clicked.connect(lambda check,widget_de_tache=widget_de_tache:tager_fait_ou_non(check,widget_de_tache))
                    #ajout de la tache au layout
                    
                    layout_des_taches.replaceWidget(label,widget_de_tache)
                    label.deleteLater()
                    widget_de_tache.leaveEvent=lambda event,valeurs=valeurs,label=label,ordre=ordre:transformer_en_label(event,valeurs,widget_de_tache,ordre)
        


    def add_arrow(event,label):
        label.setText(label.text().replace("\n ","\n▼"))
    def remove_arrow(event,label):
        label.setText(label.text().replace("\n▼","\n "))
        
     
    #chrger les daches stockées dans le fichier            
    def charger_les_taches():
        fenetre.telecharger_les_taches.hide()
        with open("liste_des_taches.txt","r")as fp:
            lignes_des_taches=fp.readlines()
        fenetre.taches_progressbar.show()
        fenetre.taches_progressbar.setMaximum(len(lignes_des_taches))
        for ordre,ligne in enumerate(lignes_des_taches):
            fenetre.taches_progressbar.setValue(fenetre.taches_progressbar.value()+1)
            statics[0]+=1
            fenetre.total_num_label.setText(f"TOTAL:\n{statics[0]}")
            valeurs=ligne.split("_")
            if len (valeurs)==5:
                titre=valeurs[0]
                date=valeurs[2]
                fait_ou_non=valeurs[4]
                if date=="1/1/1753":
                    date="--/--/----"

                if fait_ou_non=="pas Fait\n":
                    statics[2]+=1
                    fenetre.pasfait_num_label.setText(f"PAS FAIT:\n{statics[2]}")
                    
                    fenetre.fait_num_label.setText(f"FAIT:\n{statics[1]}")
                else:
                    statics[1]+=1
                    fenetre.fait_num_label.setText(f"FAIT:\n{statics[1]}")
                    fenetre.pasfait_num_label.setText(f"PAS FAIT:\n{statics[2]}")
                    


                contenu=f'{ordre+1}) Titre: {titre}{" "*(20-len(titre))}|\n               {date}'
                label=QPushButton()
                label.setStyleSheet('''QPushButton{text-align:center;background:rgb(50,50,50);border-radius:10px;color:white;font: 14pt "Consolas";border:1px solid rgb(0,0,0)}QPushButton:hover{border:1px solid rgb(255,255,255);}''')
                shadow = QGraphicsDropShadowEffect()   
                shadow.setBlurRadius(10)   
                shadow.setColor(QColor(0,0,0))  
                shadow.setOffset(0,0)  
                label.setGraphicsEffect(shadow)   
                label.setFixedHeight(80)    
                label.setText(contenu)   
                layout_des_taches.addWidget(label)
                list_des_widget_des_taches.append(valeurs)
                label.clicked.connect(lambda event,valeurs=valeurs,label=label,ordre=ordre:transformer_en_widget(event,valeurs,label,ordre))
                label.enterEvent=lambda event,label=label:add_arrow(event,label)
                label.leaveEvent=lambda event,label=label:remove_arrow(event,label)
                list_des_labels.append(label)    
        fenetre.taches_progressbar.hide()
        
        update(labels,statics,labels_golbal,statistics_global)     

    #ajouter une tache apres la confirmation dans la dialog d'ajout
    def confirmer_lajout_dune_tache():
        #recuperer les valeur
        titre=dialog_dajout.titre.text()
        objectif=dialog_dajout.objectif.toPlainText()
        date=dialog_dajout.date.date()
        date=f"{date.day()}/{date.month()}/{date.year()}"
        importance=dialog_dajout.importanceslider.value()

                
        #telechrger la widget des taches
        widget_de_tache=QWidget()
        loadUi("taskwidget.ui",widget_de_tache)
        widget_de_tache.setFixedHeight(156)
        
        # faire un effet d'ambre pour les sous widget de la widget de tache 
        listy=[widget_de_tache,widget_de_tache.objectif,widget_de_tache.date,widget_de_tache.fait_button,widget_de_tache.clear,widget_de_tache.faitounontag,widget_de_tache.title]
        for component in listy:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0,0,0))  
            shadow.setOffset(0,0)
            component.setGraphicsEffect(shadow)
        #afficter les valeur
        widget_de_tache.importancelabel.setText(f"{importance}%")
        widget_de_tache.title.setText(titre)
        if date=="1/1/1753":
            date="--/--/----"
        widget_de_tache.date.setText(date)
        widget_de_tache.objectif.setText(objectif)
        widget_de_tache.ordre_ou_nouveau.setIcon(QIcon("new.png"))
        widget_de_tache.ordre_ou_nouveau.setStyleSheet("")
        #########
        #ajouter la widget a la liste des widget des tache
        list_des_widget_des_taches.insert(0,widget_de_tache)
        list_des_labels.insert(0,[])
        #tager la tache comme pas fait evidamment et incrementer les statistiques
        statics[0]+=1
        fenetre.total_num_label.setText(f"TOTAL:\n{statics[0]}")
        statistics_global[0]+=1
        statistics_global[2]+=1
        tager_fait_ou_non(False,widget_de_tache,True)
        #regler le bouton "clear" pour efaccer la tache correspendante
        index=list_des_widget_des_taches.index(widget_de_tache)
        widget_de_tache.clear.clicked.connect(lambda check,index=index:demander_la_confirmation_pour_la_suppression(index))
        
        #ajout de la tache a la scroll area 
        layout_des_taches.insertWidget(0,widget_de_tache)
        widget_du_layout_des_taches.setLayout(layout_des_taches)
        fenetre.taskscrollarea.setWidget(widget_du_layout_des_taches)
        #pour tager une tache comme fait
        widget_de_tache.fait_button.clicked.connect(lambda check,widget_de_tache=widget_de_tache:tager_fait_ou_non(check,widget_de_tache))
        update(labels,statics,labels_golbal,statistics_global)
    #charger les statistique et les taches dans les fichier text correspendants   
    def enregistrer_les_statistiques_et_les_taches(event):
        #charger les stats
        with open("statistiques_des_taches.txt","w") as fp:
            fp.write(f"{statistics_global[0]}_{statistics_global[1]}_{statistics_global[2]}_{statistics_global[3]}")
        #charger les taches :
        with open ("liste_des_taches.txt","w") as fp:
            lignes=[]
            for widget_de_tache in list_des_widget_des_taches:
                if type(widget_de_tache)!=type([]):
                    titre=widget_de_tache.title.text()
                    objectif=widget_de_tache.objectif.toPlainText().replace("\n","#")
                    date=widget_de_tache.date.text()
                    importance=widget_de_tache.importancelabel.text().replace("%","")
                    fait_ou_non=widget_de_tache.faitounon.text()
                else:
                    valeurs=widget_de_tache
                    titre=valeurs[0]
                    objectif=valeurs[1]
                    date=valeurs[2]
                    importance=valeurs[3]
                    fait_ou_non=valeurs[4]
                ligne=f"{titre}_{objectif}_{date}_{importance}_{fait_ou_non}"
                lignes.append(ligne)
            lignes_triées=sorted(lignes, key=lambda x: int(x.split('_')[-2]),reverse=True)
            lignes_triées=sorted(lignes_triées, key=lambda x: x.split('_')[-1],reverse=True)
            for ligne in lignes_triées:
                fp.write(ligne)
        #lever la notification pour confirmer le bien sauvgardement et empecher le spam du 
        #bouton de sauvegardement 
        fenetre.save_les_taches.setEnabled(False)
        def disable():
            fenetre.save_les_taches.setEnabled(True)
        QTimer.singleShot(3000,disable)
        lever_une_notif("enregistré avec succès !",2000)

    ###############"
    def renitialiser_lhistorique_des_taches():
        statistics_global[0]=statics[0]
        statistics_global[1]=statics[1]
        statistics_global[2]=statics[2]
        statistics_global[3]=0
        update(labels,statics,labels_golbal,statistics_global)
    ######
    def effectuer_une_recherche(type_):
        list_des_titres=[]
        list_des_objectifs=[]
        list_des_dates=[]
        max_titre_len=0
        max_objectif_len=0
        list_des_widgets_touvés_par_le_recherche.clear()
        list_des_items.clear()
        fenetre.taches_recherche_list.clear()
        if type_=="text":
            source=fenetre.recherche_text.text()
        else:
            date=fenetre.recherche_date.date()
            source=f"{date.day()}/{date.month()}/{date.year()}"
        if source!="":
            for i,widget in enumerate(list_des_widget_des_taches):
                if type(widget)!=type([]):
                    objectif=widget.objectif.toPlainText()
                    titre=widget.title.text()
                    date=widget.date.text()
                else:
                    valeurs=widget
                    widget=list_des_labels[i]
                    titre=valeurs[0]
                    objectif=valeurs[1]
                    date=valeurs[2]
                
                if objectif=="":
                    objectif="sans details"
                if titre=="":
                    titre="sans titre"
                if date=="":
                    date="sans date"
                
                trouvé=False
                if type_=="date":
                    if source==date:
                        trouvé=True
                else:
                    if source in objectif or source in titre:
                        trouvé=True
                if trouvé :
                    list_des_widgets_touvés_par_le_recherche.append(widget)
                    list_des_titres.append(titre)
                    list_des_objectifs.append(objectif)
                    list_des_dates.append(date)
                    if len(titre)>max_titre_len:
                        max_titre_len=len(titre)
                    if len(objectif)>max_objectif_len:
                        max_objectif_len=len(objectif)
            for i in range(len(list_des_dates)):
                
                item=list_des_titres[i]+"*"*(max_titre_len-len(list_des_titres[i]))+" | "+list_des_objectifs[i]+" "*(max_objectif_len-len(list_des_objectifs[i]))+" | "+list_des_dates[i]
                fenetre.taches_recherche_list.addItem(item)
                list_des_items.append(item)
        else:
            fenetre.taches_recherche_list.clear()
    def selectionner_une_tache():
        key=fenetre.taches_recherche_list.selectedItems()[0].text()
        index=list_des_items.index(key)
        widget_à_selectionner=list_des_widgets_touvés_par_le_recherche[index]
        for widget in list_des_widgets_touvés_par_le_recherche:
            if widget==widget_à_selectionner:
                #scroller jusqua la tache
                max_scroll=fenetre.taskscrollarea.verticalScrollBar().maximum()
                min_scroll=fenetre.taskscrollarea.verticalScrollBar().minimum()
                
                scroll_distance=max_scroll-min_scroll
                len_=len(list_des_widget_des_taches)
                if type(widget)==type(QPushButton()) or type(widget)==type([]):
                    i=(len_-1)-list_des_labels.index(widget_à_selectionner)    
                else:
                    i=(len_-1)-list_des_widget_des_taches.index(widget_à_selectionner)

                pas=scroll_distance/(len_)
                fenetre.taskscrollarea.verticalScrollBar().setValue(int(pas*(len_-(i)-(i+1)/len_)))
                #####

                def clignioter(n):
                    if n%2==0:
                        if  type(widget)==type(QPushButton()):
                            
                            widget_à_selectionner.setStyleSheet(widget_à_selectionner.styleSheet().replace("color:white","color:rgb(152,31,31)"))
                            widget_à_selectionner.setStyleSheet(widget_à_selectionner.styleSheet().replace("border:0px;","border:2px solid white;"))
                                                   
                    else:
                        if  type(widget)==type(QPushButton()):
                            widget_à_selectionner.setStyleSheet(widget_à_selectionner.styleSheet().replace("color:rgb(152,31,31)","color:white"))
                            widget_à_selectionner.setStyleSheet(widget_à_selectionner.styleSheet().replace("border:2px solid white;","border:0px;"))
                        
                for i in range(20):
                    QTimer.singleShot(100*(i),lambda n=i:clignioter(n))
            else:
                widget.setStyleSheet(widget.styleSheet().replace("border:2px solid white;","border:0px;"))
        
            
    ############
    #afficher l'aimpotance dans la fenetre d'ajout
    dialog_dajout.importanceslider.valueChanged.connect(lambda:dialog_dajout.importancelabel.setText(f"importance:{dialog_dajout.importanceslider.value()}%"))
    #aafficher la fenetre d'ajout d'une tache
    fenetre.add_task_button.clicked.connect(ajouter_une_tache)
    #confirmer l'ajout d'une tache
    dialog_dajout.confirmer.clicked.connect(confirmer_lajout_dune_tache)
    ######
    #creer le layout de la scroll area des taches
    layout_des_taches=QVBoxLayout()
    widget_du_layout_des_taches=QWidget()
    widget_du_layout_des_taches.setLayout(layout_des_taches)
    fenetre.taskscrollarea.setWidget(widget_du_layout_des_taches)
    #la liste des widgets des taches:
    list_des_widget_des_taches=[] 
    #creons une figure matplotlib et pour afficher le graphe de l'acceuille 
    fig = Figure(facecolor=(0,0,0,0))
    ax = fig.add_subplot(121,facecolor=(0,0,0,0))
    ax_global=fig.add_subplot(122,facecolor=(0,0,0,0))
    ax.set_title("les statistiques\nactuelles")

    ax.spines[:].set_color("white")
    ax.spines[:].set_linewidth(2)
    ax_global.spines[:].set_color("white")
    ax_global.spines[:].set_linewidth(2)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0,0,0))  
    shadow.setOffset(2,0)
    fenetre.graphe_acc_label.setGraphicsEffect(shadow)
    ##########
    fenetre.taches_recherche_list.doubleClicked.connect(selectionner_une_tache)
    ###################################################
    #pour le recherche
    list_des_widgets_touvés_par_le_recherche=[]
    list_des_items=[]
    list_des_labels=[]
    fenetre.recherche_text.textChanged.connect(lambda check, type="text":effectuer_une_recherche(type))
    fenetre.confirmer_recherche_par_date.clicked.connect(lambda check, type="date":effectuer_une_recherche(type))
    scrollbar_vertical = fenetre.taches_recherche_list.horizontalScrollBar()       
    scrollbar_vertical.setStyleSheet( """QScrollBar:horizontal {background-color: white;height: 10px;}
                                         QScrollBar::handle:horizontal {background-color: #999999;min-width: 20px;}
                                         QScrollBar::handle:horizontal:hover {background-color: rgb(152,31,31);}
                                         QScrollBar::handle:horizontal:pressed {background-color: rgb(152,31,31);}"""
                                    )
    ##les variable pour les statiques des tache (et chargement des valeurs)
    labels=["total","fait","pas\nfait"] 
    statics=[0,0,0]   
    labels_golbal=["total","fait","pas\nfait","supprimé"]

    with open("statistiques_des_taches.txt","r") as fp:
        l=fp.readline()
        valeurs=l.split("_")
        statistics_global=[int(valeurs[0]),int(valeurs[1]),int(valeurs[2]),int(valeurs[3])]
    #charger les taches stockées
    fenetre.telecharger_les_taches.clicked.connect(charger_les_taches)
    ###################
    #associer une animation a la widget des notification et des ambres
    listy=[fenetre.logo_notif_widget,fenetre.hide_notif_widget_button,fenetre.notif_widget,fenetre.message_notif_widget]
    for component in listy:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0,0,0))  
        shadow.setOffset(1,3)
        component.setGraphicsEffect(shadow)
    
    #renitailiser l'historique des taches:
    fenetre.reni_histo.clicked.connect(renitialiser_lhistorique_des_taches)
    #pour sauvgarder les changement
    fenetre.save_les_taches.clicked.connect(enregistrer_les_statistiques_et_les_taches)
    

    
    
########################### fin de la fonction home page ###################
#############################################################################

#############################################################################
# fonction de la page des calcules 
#############################################################################
def calculator_page():
    global first_time_in_calc_page
    if first_time_in_calc_page: 
        #ajouter une formule
        def show_dialog_dajout_dune_formule():
            dialog_dajout_dune_formule.titre.setText("")
            dialog_dajout_dune_formule.formule.setText("")
            dialog_dajout_dune_formule.show()
            
        def extracter_les_facteurs(widget_de_formule):
            list_des_facteurs_=[]
            formule=widget_de_formule.info_formule.toolTip()
            facteur=""
            cetait_un_alphab=False
            for caractere in formule:
                if caractere.isalpha() or caractere=="_" or (cetait_un_alphab and caractere.isdigit()):
                    cetait_un_alphab=True
                    facteur+=caractere
                else:
                    cetait_un_alphab=False
                    if facteur!="" and facteur not in list_des_facteurs_:
                        list_des_facteurs_.append(facteur)
                    facteur=""
            if facteur!=""and (facteur not in list_des_facteurs_):
                list_des_facteurs_.append(facteur)
            return list_des_facteurs_
        def anticlick(check,btn):
            if check:
                btn.setChecked(False)
            else:
                btn.setChecked(True)
                
        #fonction pour effacer une formule
        def effacer_une_formule(widget_de_formule):
            if widget_de_formule.ordre.isChecked():
                fenetre.nomdelaformuleencours.setText("calculatrice classique")
                fenetre.facteur_name.setText("entrer une operation")
                fenetre.facteur_valeur.setText("")
                fenetre.afficheur.setText("")
                fenetre.precedant.setEnabled(False)
                fenetre.suivant.setEnabled(False)
            if fenetre.principal_wid_calc_2.height()!=211:
                wid2animation.increase_height(-70,1)
                wid3animation.increase_height(70,1,"u")
                fenetre.suivant.setText("suivant")
        
        def passer_au_mode_classique():
                if  fenetre.principal_wid_calc_2.height()==281:
                    wid2animation.increase_height(-70,1)
                    wid3animation.increase_height(70,1,"u")
                fenetre.facteur_name.setText("entrer une operation")
                fenetre.nomdelaformuleencours.setText("calculatrice classique")
                fenetre.facteur_valeur.setText("")
                fenetre.afficheur.setText("")
                fenetre.precedant.setEnabled(False)
                fenetre.suivant.setEnabled(False)             

                    
        #ajouter une tache apres la confirmation dans la dialog d'ajout
        def ajouter_une_formule(titre_fich="",formule__fich="",a_partir_du_fichier=False):
            #recuperer les valeur
            if not a_partir_du_fichier:
                titre=dialog_dajout_dune_formule.titre.text()
                formule=dialog_dajout_dune_formule.formule.text()
            else:
                titre=titre_fich
                formule=formule__fich
            nombre_des_lettres_alpha=0 
            try:
                dialog_dajout_dune_formule.error.setText("")
                formule_de_test=""
                for letter in formule:
                    if letter.isalpha() or letter=="_" :
                        
                        nombre_des_lettres_alpha+=1
                        formule_de_test+="1"
                    else:
                        formule_de_test+=letter
                if formule_de_test.isdigit() or nombre_des_lettres_alpha==0:
                    formule_de_test+="***"
                s=eval(formule_de_test) 
                #telechrger la widget des taches
                widget_de_formule=QWidget()
                loadUi("formule_widget.ui",widget_de_formule)
                widget_de_formule.setFixedHeight(204)
                
                ###
                #pour marker la formule en train d'etre executer
                widget_de_formule.lancer.clicked.connect(lambda check,widget_de_formule=widget_de_formule:lancer_une_formule(widget_de_formule))
                widget_de_formule.ordre.clicked.connect(lambda check ,btn=widget_de_formule.ordre:anticlick(check,btn))
                #pour effacer la formule
                widget_de_formule.delete_.clicked.connect(lambda check ,widget_de_formule=widget_de_formule:effacer_une_formule(widget_de_formule))

                
                #afficher la formule en utilisant la tooltip d'un bouton 
                widget_de_formule.info_formule.setToolTip(formule)
                # faire un effet d'ambre pour les sous widget de la widget de fomule
                listy=[widget_de_formule,widget_de_formule.lancer,widget_de_formule.delete_,widget_de_formule.titre,widget_de_formule.ordre]
                for component in listy:
                    shadow = QGraphicsDropShadowEffect()
                    shadow.setBlurRadius(10)
                    shadow.setColor(QColor(0,0,0))  
                    shadow.setOffset(0,0)
                    component.setGraphicsEffect(shadow)
                #afficter les valeur
                titre=f'<html><head/><body><p align="center">{titre} </p></body></html>'
                widget_de_formule.titre.insertHtml(titre)
                #########
                #ajouter la widget a la liste des widget des tache
                list_des_widget_des_Formules.append(widget_de_formule)
                list_des_lists_des_facteurs.append(extracter_les_facteurs(widget_de_formule))
                #ajout de la tache a la scroll area 
                layout_des_formules.insertWidget(0,widget_de_formule)
                widget_du_layout_des_formules.setLayout(layout_des_formules)
                fenetre.srollareadesformules.setWidget(widget_du_layout_des_formules)
            except:
                if not a_partir_du_fichier:
                    dialog_dajout_dune_formule.error.setText("Formule invalide !")

        def effacer_un_resultat(widget_de_resultat):
            list_des_widget_des_resultats.remove(widget_de_resultat)
            
        def ajouter_un_resultat(titre_du_calcule,titre_de_la_formule,resultat,informations,date,a_partir_du_fichier=False):
            list_des_statistiques[0]+=1
            widget_de_resultat=QWidget()
            loadUi("resultat_de_calcule_widget.ui",widget_de_resultat)
            widget_de_resultat.setFixedHeight(101)
            # faire un effet d'ambre pour les sous widget de la widget de tache 
            listy=[widget_de_resultat,widget_de_resultat.resultat_nom,widget_de_resultat.resultat_valeur,widget_de_resultat.date]
            for i,component in enumerate(listy):
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(10)
                shadow.setColor(QColor(0,0,0)) 
                shadow.setOffset(0,0)
                component.setGraphicsEffect(shadow)        
            
            widget_de_resultat.info.setToolTip(informations)
            if titre_du_calcule=="":
                widget_de_resultat.resultat_nom.setText(titre_de_la_formule)
            else:
                widget_de_resultat.resultat_nom.setText(titre_du_calcule)
            
            widget_de_resultat.date.setText(date)
            widget_de_resultat.resultat_valeur.setText(resultat)
            list_des_widget_des_resultats.append(widget_de_resultat)
            if a_partir_du_fichier:
                widget_de_resultat.epingler.setChecked(True)
            widget_de_resultat.delete_.clicked.connect(lambda check,widget_de_resultat=widget_de_resultat:effacer_un_resultat)
            layout_des_resultats.insertWidget(0,widget_de_resultat)

            widget_du_layout_des_resultats.setLayout(layout_des_resultats)
            fenetre.scrollareadesresultats.setWidget(widget_du_layout_des_resultats) 
            ####reglage des statistiques:
            if titre_de_la_formule in list_des_titres_des_formules:
                index=list_des_titres_des_formules.index(titre_de_la_formule)
                list_des_statistiques[index]+=1
            else:
                list_des_statistiques.append(1)
                list_des_titres_des_formules.append(titre_de_la_formule)
            contenu=""
            for i in range(len(list_des_statistiques)):
                contenu+=f'   {list_des_titres_des_formules[i]}:<span style="font-size:20pt; color:#981f1f;"> {list_des_statistiques[i]}</span>'   

            statLabel.setText(contenu)

            
                
            
              

        def get_formatted(formule,les_facteurs,facteur_actuel):
            les_facteurs_=sorted(les_facteurs,key=lambda x:len(x),reverse=True)

            formule_hachtaged_=formule
            for facteur in les_facteurs_:
                if facteur!=facteur_actuel and facteur not in facteur_actuel :
                    formule_hachtaged_=formule_hachtaged_.replace(facteur,"#"*len(facteur))
            facteur_actuel_formatted=f'<span style="font-size:20pt; color:#981f1f;">  {facteur_actuel}  </span>'
            cache="?"*len(facteur_actuel)
            formule_hachtaged_=formule_hachtaged_.replace(facteur_actuel,cache)
            for i in range(len(formule)):
                car_actu=formule_hachtaged_[i]
                if car_actu=="#":
                    formule_hachtaged_=formule_hachtaged_.replace(car_actu,formule[i],1)

            
            formule_formatted=f'<html><head/><body><p align="center">{formule_hachtaged_} </p></body></html>'
            formule_formatted_finale=formule_formatted.replace(cache,facteur_actuel_formatted)
            #pour le "-" et le "\"car ils poseent des problemes
            for i in range(len(formule_formatted_finale)):
                car=formule_formatted_finale[i]
                if car=="-" and formule_formatted_finale[i+1:i+5]=="size" and formule_formatted_finale[i-4:i]=="font":
                    formule_formatted_finale=formule_formatted_finale[0:i]+"?"+formule_formatted_finale[i+1:]

                              
            formule_formatted_finale=formule_formatted_finale.replace("-",'<span style="font-size:12pt; color:green;"> - </span>')
            formule_formatted_finale=formule_formatted_finale.replace('?',"-")    
            for i in range(len(formule_formatted_finale)):
                car=formule_formatted_finale[i]            
                if car=="/" and formule_formatted_finale[i-1]=="<":
                    formule_formatted_finale=formule_formatted_finale[0:i]+"@"+formule_formatted_finale[i+1:]  
            formule_formatted_finale=formule_formatted_finale.replace("/",'<span style="font-size:12pt; color:green;"> / </span>')
            formule_formatted_finale=formule_formatted_finale.replace('@',"/")
            #]#############""
            
            
            formule_formatted_finale=formule_formatted_finale.replace("(",'<span style="font-size:12pt; color:yellow;"> ( </span>')
            formule_formatted_finale=formule_formatted_finale.replace(")",'<span style="font-size:12pt; color:yellow;"> ) </span>')
            formule_formatted_finale=formule_formatted_finale.replace("+",'<span style="font-size:12pt; color:green;"> + </span>')
            formule_formatted_finale=formule_formatted_finale.replace("*",'<span style="font-size:12pt; color:green;"> * </span>')
            
     
            return formule_formatted_finale 
            
        
        
        def recommencer_le_calcule(widget_de_formule):

            fenetre.precedant.setEnabled(False)
            global curseur_dans_les_list_des_facteurs, curseur_dans_les_facteurs
            curseur_dans_les_facteurs=0
            titre_de_la_formule=widget_de_formule.titre.toPlainText()
            fenetre.nomdelaformuleencours.setText(titre_de_la_formule)
            formule=widget_de_formule.info_formule.toolTip()
            curseur_dans_les_list_des_facteurs=list_des_widget_des_Formules.index(widget_de_formule)
            les_facteurs=list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs]
            premier_facteur=les_facteurs[0]
            fenetre.facteur_name.setText(premier_facteur)
            fenetre.afficheur.setText("")
            ########♦"

            formatted=get_formatted(formule,les_facteurs,premier_facteur)                 
            fenetre.afficheur.insertHtml(formatted)

            if len(list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs])==1 and fenetre.principal_wid_calc_2.height()!=281:
                fenetre.suivant.setText("Finir")
                wid2animation.increase_height(70,1)
                wid3animation.increase_height(-70,1,"u")
            elif fenetre.principal_wid_calc_2.height()!=211 and len(list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs])!=1:
                wid2animation.increase_height(-70,1)
                wid3animation.increase_height(70,1,"u")
                fenetre.suivant.setText("suivant")
                
            if len(list_des_valeurs)<len(list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs]):
                for _ in range(len(list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs])):
                    list_des_valeurs.append("")


        #une fonction pour marker une seule formule en cours
        def lancer_une_formule(widget_de_formule):
            fenetre.suivant.setEnabled(True)
            widget_de_formule.ordre.setChecked(True)
            recommencer_le_calcule(widget_de_formule)
            
            for widget in list_des_widget_des_Formules:
                if widget!=widget_de_formule:
                    widget.ordre.setChecked(False)

        def suivant():
            try:
                fenetre.facteur_valeur.setFocus(True)
                valeur_recuperée=str(eval(fenetre.facteur_valeur.text()))
                fenetre.precedant.setEnabled(True)
                global curseur_dans_les_facteurs,curseur_dans_les_list_des_facteurs
                curseur_dans_les_facteurs=curseur_dans_les_facteurs+1
                les_facteurs=list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs]
                widget_de_formule_actuelle=list_des_widget_des_Formules[curseur_dans_les_list_des_facteurs]
                formule=widget_de_formule_actuelle.info_formule.toolTip()
                if curseur_dans_les_facteurs==len(les_facteurs)-1 and fenetre.suivant.text()!="Finir" :
                    if fenetre.extendresults.isChecked():
                        fenetre.extendresults.setChecked(False)
                        extend_les_resultats()
                    fenetre.suivant.setText("Finir")
                    wid2animation.increase_height(70,1)
                    wid3animation.increase_height(-70,1,"u")
                if curseur_dans_les_facteurs>=len(les_facteurs):
                    list_des_valeurs[curseur_dans_les_facteurs-1]=valeur_recuperée
                    
                    recommencer_le_calcule(widget_de_formule_actuelle)

                    
                    titre_du_calcule=fenetre.titre_du_calcule_valeur.text()
                    fenetre.titre_du_calcule_valeur.setText("")
                    titre_de_la_formule=widget_de_formule_actuelle.titre.toPlainText()
                    
                    informations=str(datetime.now().time())[0:5]+f"\n[{titre_de_la_formule}]\n"

                    zipped_data=zip(les_facteurs,list_des_valeurs)
                    sorted_data=sorted(zipped_data,key=lambda x:len(x[0]),reverse=True)
                    les_facteurs_triés=[i[0] for i in sorted_data]
                    list_des_valeurs_triés=[i[1] for i in sorted_data]

                    for i in range(len(les_facteurs_triés)):
                        formule=formule.replace(les_facteurs_triés[i],list_des_valeurs_triés[i])
                        informations+=les_facteurs_triés[i]+":"+list_des_valeurs_triés[i]+"\n"
                    resultat=str(eval(formule))

                    date=str(datetime.now().date())
                    ajouter_un_resultat(titre_du_calcule,titre_de_la_formule,resultat,informations,date)

                    for i in range(len(list_des_valeurs)):
                        list_des_valeurs[i]=""
                else:
                    facteur_actuel=les_facteurs[curseur_dans_les_facteurs]
                    fenetre.facteur_name.setText(facteur_actuel)
                    fenetre.afficheur.setText("")
                    formatted=get_formatted(formule,les_facteurs,facteur_actuel)
                    

                    fenetre.afficheur.insertHtml(formatted)
                    list_des_valeurs[curseur_dans_les_facteurs-1]=valeur_recuperée

                fenetre.facteur_valeur.setText((list_des_valeurs[curseur_dans_les_facteurs]))
            except:
                fenetre.facteur_valeur.setText("valeur invalide")

        
        def precedant():
            fenetre.facteur_valeur.setFocus(True)
            global curseur_dans_les_facteurs,curseur_dans_les_list_des_facteurs
            widget_de_formule_actuelle=list_des_widget_des_Formules[curseur_dans_les_list_des_facteurs]
            formule=widget_de_formule_actuelle.info_formule.toolTip()

            if fenetre.suivant.text()=="Finir":
                wid2animation.increase_height(-70,1)
                wid3animation.increase_height(70,1,"u")                
            
            curseur_dans_les_facteurs=curseur_dans_les_facteurs-1
            fenetre.suivant.setText("Suivant")
            les_facteurs=list_des_lists_des_facteurs[curseur_dans_les_list_des_facteurs]
            facteur_actuel=les_facteurs[curseur_dans_les_facteurs]
            fenetre.afficheur.setText("")
            formatted=get_formatted(formule,les_facteurs,facteur_actuel)
            fenetre.afficheur.insertHtml(formatted)
            fenetre.facteur_name.setText(facteur_actuel)
            fenetre.facteur_valeur.setText((list_des_valeurs[curseur_dans_les_facteurs]))
            if curseur_dans_les_facteurs==0:
                fenetre.precedant.setEnabled(False)
                
        #pour charger les formules enregistrée dans le fichier 
        def charger_les_formules():
            fenetre.telecharger_les_formules.hide()
            with open("liste_des_formules.txt","r") as fp:
                lignes=fp.readlines()
                fenetre.formules_progressbar.setMaximum(len(lignes))
                for ligne in lignes:
                    fenetre.formules_progressbar.setValue(fenetre.formules_progressbar.value()+1)
                    valeurs=ligne.split("#")
                    titre=valeurs[0]
                    formule=valeurs[1].replace("\n","")
                    ajouter_une_formule(titre,formule,a_partir_du_fichier=True)
                fenetre.formules_progressbar.hide()    
                
        #pour charger les formules dans le fichier texte 
        def enregistrer_les_formules():
            with open("liste_des_formules.txt","w") as fp:
                for widget_de_formule in list_des_widget_des_Formules:
                    if not widget_de_formule.delete_.isChecked():
                        titre=widget_de_formule.titre.toPlainText()
                        formule=widget_de_formule.info_formule.toolTip()
                        ligne=f"{titre}#{formule}\n"
                        fp.write(ligne)
            #lever la notification pour confirmer le bien sauvgardement et empecher le spam du 
            #bouton de sauvegardement 
            fenetre.save_les_formules.setEnabled(False)
            def disable():
                fenetre.save_les_formules.setEnabled(True)
            QTimer.singleShot(3000,disable)
            lever_une_notif("enregistré avec succès !",2000)
        def enregistrer_les_resultats():
            with open("liste_des_calcules.txt","w") as fp:
                for widget_de_resultat in list_des_widget_des_resultats:
                    if widget_de_resultat.epingler.isChecked():
                        nom= widget_de_resultat.resultat_nom.text()
                        informations=widget_de_resultat.info.toolTip().replace("\n","%")
                        date=widget_de_resultat.date.text()
                        resultat=widget_de_resultat.resultat_valeur.toPlainText()
                        ligne=f"{nom}#{resultat}#{date}#{informations}\n"
                        fp.write(ligne)
            fenetre.save_les_resultats.setEnabled(False)
            fenetre.save_les_formules.setEnabled(False)
            def disable():
                fenetre.save_les_formules.setEnabled(True)
                fenetre.save_les_resultats.setEnabled(True)
            QTimer.singleShot(3000,disable)
            lever_une_notif("enregistré avec succès !",2000) 
        def charger_les_resultats():
            fenetre.telecharger_les_resultats.hide()
            with open("liste_des_calcules.txt","r") as fp:
                lignes=fp.readlines()
            fenetre.resultats_progressbar.setMaximum(len(lignes))
            for ligne in lignes:
                fenetre.resultats_progressbar.setValue(fenetre.resultats_progressbar.value()+1)
                valeurs=ligne.split("#")
                titre_du_calcule=valeurs[0]
                resultat=valeurs[1]
                date=valeurs[2]
                informations=valeurs[3].replace("\n","").replace("%","\n")
                titre_de_la_formule=informations.split("\n")[1][1:-1]
                ajouter_un_resultat(titre_du_calcule,titre_de_la_formule,resultat,informations,date,True)
            fenetre.resultats_progressbar.hide()
        def extend_les_resultats():
            if fenetre.principal_wid_calc_2.height()==211 :
                if fenetre.extendresults.isChecked():
                    cadreanimation.increase_height(210,1)
                    scrollanimation.increase_height(210,1)
                else:
                    cadreanimation.increase_height(-210,1)
                    scrollanimation.increase_height(-210,1)
                fenetre.extendresults.setEnabled(False)
                QTimer.singleShot(500,lambda:fenetre.extendresults.setEnabled(True))
            else:
                fenetre.extendresults.setChecked(False)
                lever_une_notif("veuillez finir l'operation en cours SVP!",1000)
                fenetre.extendresults.setEnabled(False)
                QTimer.singleShot(2000,lambda:fenetre.extendresults.setEnabled(True))
            
        ##  ###               
        def Enter_click_au_lieu_de_suivant(event):
            if (fenetre.facteur_valeur.hasFocus() or fenetre.titre_du_calcule_valeur.hasFocus()) and fenetre.suivant.isEnabled():
                #pour naviguer entre les deux lineEdit si c'est possible 
                #avec les deux flesh up et down
                if event.key()==Qt.Key_Down and fenetre.suivant.text()=="Finir":
                    fenetre.titre_du_calcule_valeur.setFocus(True)
                elif event.key()==Qt.Key_Up and fenetre.suivant.text()=="Finir":
                    fenetre.facteur_valeur.setFocus(True)
                #le bouron Entrer
                elif event.key()== 16777220:
                    suivant()
            
                    
                
        fenetre.keyPressEvent=Enter_click_au_lieu_de_suivant                
        ####
        #####
        #pour les operation classique
        def afficher_le_resultat_d_une_operation_classique():
            if fenetre.nomdelaformuleencours.text()=="calculatrice classique":
                operation=fenetre.facteur_valeur.text()
                try:
                    resultat=str(eval(operation))
                    fenetre.afficheur.setText("")
                    fenetre.afficheur.insertHtml(f'<span style="font-size:30pt; color:white;"> {resultat}</span>')
                except:
                    fenetre.afficheur.setText("...")
                
         
        def recommencer_le_calcule_par_le_bouton():
            for widget_de_formule in list_des_widget_des_Formules:
                if widget_de_formule.ordre.isChecked():
                    recommencer_le_calcule(widget_de_formule)
                 
         
         
            
        fenetre.save_les_formules.clicked.connect(enregistrer_les_formules)
        fenetre.save_les_resultats.clicked.connect(enregistrer_les_resultats)
        
        fenetre.reni_le_calcule.clicked.connect(recommencer_le_calcule_par_le_bouton)
        curseur_dans_les_list_des_facteurs=0
        curseur_dans_les_facteurs=0
        list_des_lists_des_facteurs=[]
        list_des_valeurs=[]
        #creer le layout de la scroll area des Formules
        layout_des_formules=QVBoxLayout()
        widget_du_layout_des_formules=QWidget()
        #creer le layout de la scroll area des resultats
        layout_des_resultats=QVBoxLayout()
        widget_du_layout_des_resultats=QWidget()
        #################les animation de fin d'un calcul pour ajouter un titre:
        wid2animation=myAnimation(fenetre.principal_wid_calc_2)
        wid3animation=myAnimation(fenetre.principal_wid_calc_3)
        ##################les animations de l'extend de la scroll area des resultats 
        cadreanimation=myAnimation(fenetre.cadredelascrollareadesresultats)
        scrollanimation=myAnimation(fenetre.scrollareadesresultats)
        ##########
        #le bouton de l'animation de la scroll area des resultats 
        fenetre.extendresults.clicked.connect(extend_les_resultats)
        #creer les axes pour l'affichage des statistiques 
        fig = Figure(facecolor=(0,0,0,0))
        ax = fig.add_subplot(111,facecolor=(0,0,0,0))
        ax.spines[:].set_color("white")
        ax.spines[:].set_linewidth(2)
        list_des_widget_des_Formules=[]
        list_des_widget_des_resultats=[]
        list_des_statistiques=[0]
        list_des_titres_des_formules=["Total "]
        #creer le label d'affichage des statistiques:
        statLabel=QLabel()
        layout=QVBoxLayout()
        statLabel.setStyleSheet('text-align:center;color: rgb(255, 255, 255);font: 16pt "Gill Sans Ultra Bold Condensed";')
        statWidget=QWidget()
        layout.addWidget(statLabel)
        statWidget.setLayout(layout)
        fenetre.scrollareadesstistiquesdecalc.setWidget(statWidget)
        scrollbar_vertical = fenetre.scrollareadesstistiquesdecalc.horizontalScrollBar()       
        scrollbar_vertical.setStyleSheet( """
    QScrollBar:horizontal {
        background-color: white;
        height: 10px;
        
    }
    
    QScrollBar::handle:horizontal {
        background-color: #999999;
        min-width: 20px;

    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: rgb(152,31,31);
    }
    
    QScrollBar::handle:horizontal:pressed {
        background-color: rgb(152,31,31);
    }
    

    
    

"""
)
        #charger les données stockées
        fenetre.telecharger_les_formules.clicked.connect(charger_les_formules)
        fenetre.telecharger_les_resultats.clicked.connect(charger_les_resultats)
        ################""
        dialog_dajout_dune_formule.confirmer.clicked.connect(ajouter_une_formule)
        fenetre.add_formule_button.clicked.connect(show_dialog_dajout_dune_formule)
        fenetre.suivant.clicked.connect(suivant)
        fenetre.precedant.clicked.connect(precedant)
        fenetre.suivant.setEnabled(False)
        fenetre.precedant.setEnabled(False)
        #pour les operation classique:
        fenetre.passer_au_mode_classique.clicked.connect(passer_au_mode_classique)
        fenetre.facteur_valeur.textChanged.connect(afficher_le_resultat_d_une_operation_classique)
        
        
###########fin de la fonction de calc#############
##################################################

##################################################
##fonction pour le coté economie
#################################################
def economie():
    list_des_j_ai=[]
    list_des_j_ai_fait_sortie=[]  
    list_des_jours=[] 
    def plot():
        ax.clear()
        list_des_jours_de_plot=[]
        for i in range(len(list_des_jours)):
            list_des_jours_de_plot.append(str(list_des_jours[i]))
        for tickx in ax.xaxis.get_ticklabels():
            tickx.set_color("white")
            tickx.set_rotation(90)   
        for ticky in ax.yaxis.get_ticklabels():
            ticky.set_color("white")
        fig.set_size_inches(0.5*len(list_des_jours)+7,3.5)
        if fenetre.affichage_en_graphe_plot.isChecked(): 
            if fenetre.show_graphe_jai_button.isChecked() :
                ax.plot(list_des_jours_de_plot,list_des_j_ai,color=(31/255,152/255,31/255))
            if fenetre.show_graphe_jaifaitsortie_button.isChecked():
                ax.plot(list_des_jours_de_plot,list_des_j_ai_fait_sortie,color=(152/255,31/255,31/255))
                
        elif fenetre.affichage_en_graphe_bar.isChecked(): 
            x = arange(len(list_des_jours_de_plot))
            if fenetre.show_graphe_jai_button.isChecked() :
                ax.bar(x,list_des_j_ai,color=(31/255,152/255,31/255),width=0.3)
            if fenetre.show_graphe_jaifaitsortie_button.isChecked():
                ax.bar(x+0.3,list_des_j_ai_fait_sortie,color=(152/255,31/255,31/255),width=0.3)
            ax.set_xticks(x + 0.15, list_des_jours_de_plot)
                
                
        fig.tight_layout()
        fig.savefig("graphe.png")
        pixmap=QPixmap("graphe.png")
        label_du_graphe.setPixmap(pixmap)
        os.remove("graphe.png") 
        layout_du_graphe.addWidget(label_du_graphe)
        wid_du_graphe.setLayout(layout_du_graphe)
        fenetre.scrollareadugraphe_economie.setWidget(wid_du_graphe)
        
 
   
    def ajouter_un_label_dune_date():

        contenu=f'      |        <span style="font-size:30pt; color:white;">{str(list_des_jours[-1])}</span>                 j ai <span style="font-size:16pt; color:rgb(31,152,31);">{list_des_j_ai[-1]}</span> dt et j ai fait sortie <span style="font-size:16pt; color:rgb(152,31,31);">{list_des_j_ai_fait_sortie[-1]}</span> dt .'
        label=QLabel()
        label.setStyleSheet('text-align:center;background:rgb(50,50,50);border-radius:5px;color:white;font: 14pt "Eras Bold ITC";border:1px solid black;')
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0,0,0))  
        shadow.setOffset(0,0)
        label.setGraphicsEffect(shadow)   
        label.setFixedHeight(60)     
        label.setText(contenu)
        layout_des_dates.insertWidget(0,label)
        widget_du_layout_des_dates.setLayout(layout_des_dates)
        fenetre.scrollareadeslignes_economie.setWidget(widget_du_layout_des_dates)
        list_des_labels.append(label)
        
    listy=[25,12,10,22,21,20,14,12,5] 
    #listy=[5,12,14,20,21,22,10,12,25]
    listyy=[7,7,7,6,6,6,6,6,6]    
    def confirmer_l_ajout():
        
        j_ai=fenetre.j_ai.text()
        j_ai_fait_sortie=fenetre.j_ai_fait_sortie.text()
        if datetime.now().date() in list_des_jours:
            list_des_j_ai_fait_sortie[-1]=(float(j_ai_fait_sortie))
            list_des_j_ai[-1]=(float(j_ai))
            list_des_jours[-1]=datetime.now().date()
            label=list_des_labels[-1]
            label.setText(f'      |        <span style="font-size:30pt; color:white;">{str(list_des_jours[-1])}</span>                 j ai <span style="font-size:16pt; color:rgb(31,152,31);">{list_des_j_ai[-1]}</span> dt et j ai fait sortie <span style="font-size:16pt; color:rgb(152,31,31);">{list_des_j_ai_fait_sortie[-1]}</span> dt .')
        else:
            list_des_j_ai.append((float(j_ai)))
            list_des_j_ai_fait_sortie.append(float(j_ai_fait_sortie))
            list_des_jours.append(datetime.now().date())
            ajouter_un_label_dune_date()
        ##########


        #########
        affichage_du_total()                                                                                                                                             
         
        plot()             
    
    
    
    def affichage_du_total():
        len_=len(list_des_jours)
        total_s=0
        total_j=0
        if fenetre.depuis_check.isChecked():

            nombre_de_jours=fenetre.entre_de_depuis.value()
            i=0
            while nombre_de_jours>=0 and i<(len_-1):
                total_j+=list_des_j_ai[len_-1-i]
                total_s+=list_des_j_ai_fait_sortie[len_-1-i]
                try :
                    date_actu=list_des_jours[len_-1-i]
                    
                    date_suiv=list_des_jours[len_-1-(i+1)]
                    days_diff=(date_actu-date_suiv).days
                except:
                    days_diff=-1
                
                nombre_de_jours-=days_diff
                i+=1
            if fenetre.entre_de_depuis.value()==fenetre.entre_de_depuis.maximum():
                total_s+=list_des_j_ai_fait_sortie[0]
                total_j+=list_des_j_ai[0]
        ##########
        else:
            date_debut=fenetre.entre_date_debut.date()
            date_fin=fenetre.entre_date_fin.date()
            date_debut_existante=0
            date_fin_existante=0
            for i in range(len_):
                if date_debut<=list_des_jours[i] :
                    date_debut_existante=list_des_jours[i]
                    break
            for i in range(len_):
                if date_fin>=list_des_jours[-1-i]:
                    date_fin_existante=list_des_jours[-1-i]
                    break
            if date_debut_existante!=0 and date_fin_existante!=0:
                debut=list_des_jours.index(date_debut_existante)
                fin=list_des_jours.index(date_fin_existante)+1
                for i in range(debut,fin):
                    total_j+=list_des_j_ai[len_-1-i]
                    total_s+=list_des_j_ai_fait_sortie[len_-1-i]
        fenetre.afficheur_du_totalj.setText(f'  {str(total_j)} Dt ')
        fenetre.afficheur_du_totals.setText(f'  {str(total_s)} Dt')

      
        
        
        
    def changer_le_type_d_affichage():
        if fenetre.affichage_en_lignes.isChecked():
            fenetre.stacked_widget_economie.setCurrentWidget(fenetre.lignes)
            fenetre.show_graphe_jaifaitsortie_button.hide()
            fenetre.show_graphe_jai_button.hide()
            fenetre.recherchedunedate_economie.show()
            fenetre.confirmer_recherche.show()
        elif fenetre.affichage_en_graphe_plot.isChecked() or fenetre.affichage_en_graphe_bar.isChecked():
            plot()
            fenetre.stacked_widget_economie.setCurrentWidget(fenetre.graphe)
            fenetre.show_graphe_jaifaitsortie_button.show()
            fenetre.show_graphe_jai_button.show()
            fenetre.recherchedunedate_economie.hide()
            fenetre.confirmer_recherche.hide()
    
    def effectuer_une_recherche_par_date():
        date_entrée=fenetre.recherchedunedate_economie.text()
        trouvé=False
        for i,label in enumerate(list_des_labels):
            contenu=label.text()
            a=contenu.index('color:white;">')
            b=contenu.index('</span>')
            date=contenu[a+14:b]
            if date==date_entrée:
                max_scroll=fenetre.scrollareadeslignes_economie.verticalScrollBar().maximum()
                min_scroll=fenetre.scrollareadeslignes_economie.verticalScrollBar().minimum()
                trouvé=True
                scroll_distance=max_scroll-min_scroll
                label.setStyleSheet(label.styleSheet().replace('border:0px solid white','border:2px solid white'))
                for other in list_des_labels:
                    if label!=other:
                        other.setStyleSheet(other.styleSheet().replace('border:2px solid white','border:0px solid white'))
                len_=len(list_des_labels)
                pas=scroll_distance/(len_)
                fenetre.scrollareadeslignes_economie.verticalScrollBar().setValue(int(pas*(len_-(i)-(i+1)/len_)))
        if not trouvé:
            for label in list_des_labels:
                label.setStyleSheet(label.styleSheet().replace('border:2px solid white','border:0px solid white'))                    
    def enregistrer_les_données():
        les_dates=""
        les_jai=""
        les_jaifaitsortie=""
        for i in range(len(list_des_jours)):
            les_dates+=str(list_des_jours[i])+"_"
            les_jai+=str(list_des_j_ai[i])+"_"
            les_jaifaitsortie+=str(list_des_j_ai_fait_sortie[i])+"_"
        with open("les_données_eco.txt","w") as fp:
            fp.writelines([les_dates+"\n",les_jai+"\n",les_jaifaitsortie+"\n"])

        fenetre.save_les_donnees_eco.setEnabled(False)
        def disable():
            fenetre.save_les_donnees_eco.setEnabled(True)
        QTimer.singleShot(3000,disable)
        lever_une_notif("enregistré avec succès !",2000)

    def charger_les_données():
        with open("les_données_eco.txt","r") as fp:
            données=fp.readlines()
            if len(données)>2:
                tempo_jours=(données[0]).replace("_\n","").split("_")
                tempo_jai=données[1].replace("_\n","").split("_")
                tempo_jaifaitsortie=données[2].replace("_\n","").split("_") 
                if str(datetime.now().date()) not in tempo_jours:
                    tempo_jours.append(str(datetime.now().date()))
                    tempo_jai.append(0.0)
                    tempo_jaifaitsortie.append(0.0)
                    
        
                for i in range(len(tempo_jours)):
            
            
                    list_des_j_ai.append(float(tempo_jai[i]))
                    list_des_j_ai_fait_sortie.append(float(tempo_jaifaitsortie[i]))
                    date_parts=tempo_jours[i].split("-")
                    list_des_jours.append(date(int(date_parts[0]),int(date_parts[1]),int(date_parts[2])))
                    ajouter_un_label_dune_date()
                plot()
                ########
                j=0
                if datetime.now().date() not in list_des_jours:
                    j+=1
                    list_des_jours.append(datetime.now().date())
                max_=0
                for i in range(len(list_des_jours)-1):
                    max_+=((list_des_jours[i]-list_des_jours[i+1]).days)*-1
                fenetre.entre_de_depuis.setMaximum(max_)
                if j==1:
                    del list_des_jours[-1]
                #########



            
    
    

                
    #type d'affichage:
    fenetre.affichage_en_lignes.clicked.connect(changer_le_type_d_affichage) 
    fenetre.affichage_en_graphe_plot.clicked.connect(changer_le_type_d_affichage) 
    fenetre.affichage_en_graphe_bar.clicked.connect(changer_le_type_d_affichage)
    ########################## 
    fenetre.entre_date_debut.setDate(fenetre.entre_date_debut.minimumDate() ) 
    fenetre.entre_date_fin.setDate(datetime.now().date() ) 
    fenetre.entre_date_fin.setMaximumDate(datetime.now().date() ) 
    fenetre.entre_date_debut.dateChanged.connect(lambda:fenetre.entre_date_fin.setMinimumDate(fenetre.entre_date_debut.date()))       
    fenetre.confirmer_total.clicked.connect(affichage_du_total)  
    fenetre.confirmer_economie.clicked.connect(confirmer_l_ajout) 

    ###les widget de l'affichage du graphe  
    wid_du_graphe=QWidget()
    label_du_graphe=QLabel()
    layout_du_graphe=QVBoxLayout()
    label_du_graphe.setScaledContents(True) 
    list_des_labels=[]  
    ########## 
    #creer le layout de la scroll area 
    layout_des_dates=QVBoxLayout()
    widget_du_layout_des_dates=QWidget()
    list_des_labels=[]
    ############
    fenetre.recherchedunedate_economie.hide()
    fenetre.confirmer_recherche.hide()
    fenetre.confirmer_recherche.clicked.connect(effectuer_une_recherche_par_date)
    
    fenetre.show_graphe_jaifaitsortie_button.clicked.connect(plot)
    fenetre.show_graphe_jai_button.clicked.connect(plot)
    
    #creons une figure matplotlib et pour afficher le graphe de l'acconomie 
    fig = Figure(facecolor=(0,0,0,0))
    ax = fig.add_subplot(111,facecolor=(0,0,0,0))


    ax.spines[:].set_color("white")
    ax.spines[:].set_linewidth(4)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0,0,0))  
    shadow.setOffset(2,0)
    label_du_graphe.setGraphicsEffect(shadow)
    ######################""""
    scrollbar_vertical = fenetre.scrollareadugraphe_economie.horizontalScrollBar()       
    scrollbar_vertical.setStyleSheet( """
    QScrollBar:horizontal {
        background-color: white;
        height: 10px;
        
    }
    
    QScrollBar::handle:horizontal {
        background-color: #999999;
        min-width: 20px;

    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: rgb(152,31,31);
    }
    
    QScrollBar::handle:horizontal:pressed {
        background-color: rgb(152,31,31);
    }
    

    
    

"""
)
    charger_les_données()
    fenetre.save_les_donnees_eco.clicked.connect(enregistrer_les_données)
    
  









############################################
# programme principale                      
############################################

app = QApplication(sys.argv)
#telecharger la fenetre principale
fenetre = QMainWindow()
loadUi("taskmanager.ui", fenetre)
fenetre.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
fenetre.setFixedSize(1228,890)

###
verifier_lexistance_des_fichier()
###
#liste des widgets qu'on va les appliquer la petite ambiance
widgetlist=[fenetre.principal_wid_economie_3,fenetre.principal_wid_economie_2,fenetre.principal_wid_economie,fenetre.principal_wid_calc,fenetre.principal_wid_calc_2,fenetre.principal_wid_calc_3,fenetre.widget,fenetre.widget_2,fenetre.widget_3,fenetre.menubar,fenetre.w1,fenetre.w2,fenetre.w3,fenetre.info,fenetre.sidemenu,fenetre.quite,fenetre.led]

#Le Timeur qui change apppelle la fonction petite ambiance 
Q=QTimer()
Q.setInterval(1000)
Q.timeout.connect(petite_ambiance)
Q.start()
fenetre.led.clicked.connect(Q.start)
#creer un menu qui affiche les infos grace au QToolButton fenetre.info
info_menu=QMenu()
info_menu.setStyleSheet("background:rgb(50,50,50)")
infolineslist=["faite par :","HICHEM BELARBI","hicehmbelarbi97@gamil.com","merci !!"]
for i, text in enumerate(infolineslist):
    action = QAction(text)
    infolineslist[i]=action
    infolineslist[i].setObjectName(f"action_{i}")# Définir un nom unique pour chaque action
for action in infolineslist:
    info_menu.addAction(action)
info_menu.setStyleSheet("""QMenu{color: rgb(255, 255, 255);
font: 16pt "Gill Sans Ultra Bold Condensed";
background:rgb(50,50,50);
border:1px solid white;border-radius:3px;}
""")
fenetre.info.setMenu(info_menu)
fenetre.info.setPopupMode(QToolButton.InstantPopup)
##########################
#associer une animation a la widget de notif
notif_animation=myAnimation(fenetre.notif_widget)
#reglage des bouton de changement des pages 
first_time_in_calc_page=True
def not_first_time_in_calc_page():
    def change():
        global first_time_in_calc_page
        first_time_in_calc_page=False
    QTimer.singleShot(100,change)
fenetre.homebutton.clicked.connect(lambda: fenetre.stackedWidget.setCurrentWidget(fenetre.home))
fenetre.statbutton.clicked.connect(lambda: fenetre.stackedWidget.setCurrentWidget(fenetre.economie))
fenetre.calcbutton.clicked.connect(lambda: fenetre.stackedWidget.setCurrentWidget(fenetre.calc))
fenetre.calcbutton.clicked.connect(not_first_time_in_calc_page)
fenetre.calcbutton.clicked.connect(calculator_page)

#####################
#ouverture du side menu
sidemenu_animation=myAnimation(fenetre.sidemenu)
fenetre.opensidemenubutton.clicked.connect(hide_show_sidemenu)
###################
#charger la dialog de la confirmation:
dialog_de_confirmation=QDialog()
loadUi("dialog_de_confirmation.ui",dialog_de_confirmation)
dialog_de_confirmation.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
#charger la fenetre d'ajout des taches
dialog_dajout=QDialog()
loadUi("ajouterunetaches.ui",dialog_dajout)
dialog_dajout.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
#charger la fenetre d'ajout d'une formule
dialog_dajout_dune_formule=QDialog()
loadUi("ajouter_une_formule.ui",dialog_dajout_dune_formule)
dialog_dajout_dune_formule.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
#############
#ajouter un effet une ambre a les coposant de la dialog d'ajout d'une tache , d'une formule et la fenetre principale 
listy=[fenetre.recherche_text,fenetre.recherche_date,fenetre.taches_recherche_list,fenetre.confirmer_recherche_par_date,fenetre.confirmer_total,fenetre.afficheur_du_totalj,fenetre.afficheur_du_totals,fenetre.show_graphe_jaifaitsortie_button,fenetre.show_graphe_jai_button,fenetre.dt_label,fenetre.aujourdhui_label,fenetre.j_ai_fait_sortie,fenetre.j_ai,fenetre.confirmer_economie,fenetre.jaifaitsortie_label,fenetre.jai_label,fenetre.scrollareadesstistiquesdecalc,fenetre.afficheur,fenetre.cadredelascrollareadesresultats,fenetre.titre_du_calcule_valeur,fenetre.titre_du_calcule_label,dialog_dajout_dune_formule.confirmer,dialog_dajout_dune_formule.close_button,dialog_dajout_dune_formule.titre,dialog_dajout_dune_formule.formule,fenetre.suivant,fenetre.facteur_name,fenetre.facteur_valeur,fenetre.precedant,fenetre.total_num_label,fenetre.fait_num_label,fenetre.pasfait_num_label,dialog_dajout.titre,dialog_dajout.objectif,dialog_dajout.date,dialog_dajout.confirmer,dialog_dajout.close_button,dialog_dajout.logo,dialog_dajout.global_title]
for component in listy:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0,0,0))  
    shadow.setOffset(0,0)
    component.setGraphicsEffect(shadow)
    
##
##lancer la fonction home page
##
home_page()
#fenetre.homebutton.clicked.connect(home_page)
    
    
economie()     
##############
fenetre.show()
sys.exit(app.exec_())
