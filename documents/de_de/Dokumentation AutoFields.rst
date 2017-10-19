=======================================================
*Automatische Änderungsdaten mit dem AutoFields Plugin*
=======================================================

:Autor: Jan Gerste
:Date: $Date: 2017-10-19 10:17:45 +0000 (Thr, 19 Oct 2017) $
:Version: $Revision: 1.1 $
:Beschreibung: Einrichten automatischer **"geändert_am"** und **"geändert_von"** Einträge mit Hilfe des AutoFields Plugin


Installation
------------

Laden Sie das Plugin **AutoFields** über Ihr QGIS unter **Erweiterungen => Erweiterungen verwalten und installieren** herunter und aktivieren Sie dieses anschließend. Nach erfolgreicher Installation finden Sie unter **Vektor => AutoFields** den Menüpunkt **"AutoFields plugin..."**. Dieser öffnet das Plugin Fenster.


Einrichten der AutoFields per Import
------------------------------------

Das AutoFields Plugin bietet die Möglichkeit, vorher exportierte Field-Definitionen zu importieren. Dazu wählen Sie den Menüpunkt **Vektor => AutoFields => Import AutoFields from JSON file...**. Dies startet einen "Öffnen"-Dialog, in dem Sie die bereitgestellte Datei **autoFields_exported.json** wählen.

Es öffnet sich ein Fenster das Ihnen die betroffen Layer, Felder und eingetragenen Werte darlegt, die importiert werden. Der Pfeil unter "Assignation" wird grün dargestellt, sofern sich noch keine AutoField-Anweisung auf dem Feld befindet. Ist dies bereits der Fall wird er stattdessen in gelb dargestellt. Dies zeigt an, dass der bisherige Ausdruck bei Durchführung des Imports mit dem neuen ersetzt werden wird.

Mit der Schaltfläche **"OK"** bestätigen Sie den Vorgang. Die Autofields sind nun angelegt und lassen sich im Plugin Fenster unter dem **Tab "List of AutoFields"** wiederfinden.


Manuelles Erstellen der AutoFields
----------------------------------

Um ein neues AutoField zu definieren wählen Sie zuerst im Plugin Fenster den/die Layer aus, für die dieses Feld definiert werden soll. Per Klicken und Ziehen oder Strg + Klick können mehrere Layer gleichzeitig gewählt werden.

Wählen Sie unterhalb der Layer-Liste die Option **"Existing Field"** und suchen aus der Liste die entsprechende Feldbezeichnung (**"geändert_am"** oder **"geändert_von"**) heraus. Danach wählen sie unter **"Value or Expression"** den Ausdruck, mit dem das Feld gefüllt werden soll.

- Für **"geändert_am"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck **now()** eingeben.
	Alternativ können Sie hier auch die vordefinierte Option **"Time Stamp"** wählen, diese verhält sich gleich.

- Für **"geändert_von"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck **@user_full_name** eingeben.

Gehen Sie sicher, dass die Option **"Calculate expression on existing features"** unter dem **"Value or Expression"**-Bereich **nicht aktiv** ist, da ansonsten alle betroffenen Felder neu gesetzt werden.

Abschließend klicken Sie auf die Schaltfläche **"Save AutoFields"** am Ende des Fensters. Die AutoFields sind jetzt gesetzt.

Um die existierenden AutoFields zu betrachten und/oder zu löschen können Sie in den **Tab "List of AutoFields"** wechseln.