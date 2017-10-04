=======================================================================
*Automatische Erfassungs- und Änderungsdaten mit dem AutoFields Plugin*
=======================================================================

:Autor: Jan Gerste
:Date: $Date: 2017-09-29 13:20:23 +0000 (Fri, 29 Sep 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Einrichten automatischer **"erfasst_am"**, **"erfasst_von"**, **"geändert_am"** und **"geändert_von"** Einträge mit Hilfe des AutoFields Plugin


Installation
------------

Laden Sie das Plugin **AutoFields** über Ihr QGIS unter **Erweiterungen => Erweiterungen verwalten und installieren** herunter und aktivieren Sie dieses anschließend. Nach erfolgreicher Installation finden Sie unter **Vektor => AutoFields** den Menüpunkt **"AutoFields plugin..."**. Dieser öffnet das Plugin Fenster.


Einrichten der AutoFields
-------------------------

Das AutoFields Plugin füllt die definierten Felder bei Neuanlage bzw. Änderung des Objektes automatisch.

Um ein neues AutoField zu definieren wählen Sie zuerst im Plugin Fenster den/die Layer aus, für die dieses Feld definiert werden soll. Per Klicken und Ziehen oder Strg + Klick können mehrere Layer gleichzeitig gewählt werden.

Wählen Sie unterhalb der Layer-Liste die Option **"Existing Field"** und suchen aus der Liste die entsprechende Feldbezeichnung (**"erfasst_am"**, **"erfasst_von"**, **"geändert_am"** oder **"geändert_von"**) heraus. Danach wählen sie unter **"Value or Expression"** den Ausdruck, mit dem das Feld gefüllt werden soll.

- Für **"erfasst_am"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck `IF("erfasst_am" IS NULL, now(), "erfasst_am")` eingeben. Dies sorgt dafür, dass dieses Feld mit dem aktuellen Datum beschrieben wird, wenn es neu erfasst wird und noch leer ist.

- Für **"erfasst_von"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck `IF("erfasst_von" IS NULL, @user_full_name, "erfasst_von")` eingeben. Dies sorgt dafür, dass dieses Feld mit dem aktuellen Benutzer beschrieben wird, wenn es neu erfasst wird und noch leer ist.

- Für **"geändert_am"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck `now()` eingeben.
	Alternativ können Sie hier auch die vordefinierte Option **"Time Stamp"** wählen, dieses verhält sich gleich.

- Für **"geändert_von"** wählen Sie **"Custom Expression"** und klicken auf den **Button "..."** rechts daneben. Dieser öffnet den **Expression Builder**, in dem Sie den Ausdruck `@user_full_name` eingeben.

Gehen Sie sicher, dass die Option **"Calculate expression on existing features"** unter dem **"Value or Expression"**-Bereich nicht aktiv ist, da ansonsten alle betroffenen Felder neu gesetzt werden.

Abschließend klicken Sie auf die Schaltfläche **"Save AutoFields"** am Ende des Fensters. Die AutoFields sind jetzt gesetzt.

Um die existierenden AutoFields zu betrachten und/oder zu löschen können Sie in den **Tab "List of AutoFields"** wechseln.