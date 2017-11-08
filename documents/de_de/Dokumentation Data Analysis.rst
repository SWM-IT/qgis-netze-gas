====================================
*Beispiele der Datenanalyse in QGIS*
====================================

:Autor: Jan Gerste
:Date: $Date: 2017-10-27 10:02:13 +0000 (Fri, 27 Oct 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Darlegung diverser Möglichkeiten zur Auswertung von Daten anhand existierender QGIS Methoden


Grafische Darstellung anhand des Stils
--------------------------------------

Der **Stileditor** in QGIS bietet weitreichende Möglichkeiten, die Feldwerte und andere Variablen miteinander zu vergleichen/verrechnen und das Ergebnis grafisch verständlich darzustellen. Dazu steht Ihnen der QGIS **Ausdruckseditor** an diversen Stellen des Stileditors zur Verfügung. Um den Stileditor zu öffnen, gehen Sie in das Eigenschaften-Fenster des Layers, den Sie bearbeiten möchten (Doppelklick auf den Layer oder Rechtsklick > Eigenschaften) und wählen in der Liste auf der linken Seite die Kategorie **Stil**.

**Der Ausdruckseditor**

 Der Ausdruckseditor ist das Instrument, welches es Ihnen unter anderem ermöglicht, Stile in Abhängigkeit von verschiedenen Werten zu definieren. Er bietet die Möglichkeit, diverse Werte mithilfe mathematischer Berechnungen, logischer Vergleiche und Bedingungen sowie Konversion zwischen Variablentypen miteinander zu verknüpfen.

 So finden Sie die Feldwerte des Layers in der Rubrik **Felder und Werte** in der mittleren Spalte des Fensters. Ebenso stehen Werte wie die aktuelle Zeit und Extraktions-/Konversionsbefehle dafür (**Datum und Zeit**), Layereigenschaften wie IDs und Attribute (**Datensatz**), Geometrieattribute wie Position, Ausmaße, Lage zu anderen Geometrien, Anzahl von Objekten/Punkten/Kanten und weitere (**Geometrie**) sowie Systemvariablen wie die Ausmaße der Karte, der Dateipfad zum Projekt oder der Benutzername des aktuellen Anwenders (**Variablen**) zur Verfügung.

 Um einen Ausdruck zu erstellen doppelklicken Sie auf die jeweiligen Werte und Funktionen aus der mittleren Spalte. Deren entsprechende Repräsentation erscheint dann im Textfeld in der linken Spalte. Alternativ oder ergänzend können Sie auch das Textfeld direkt bearbeiten. Unter dem Text befindet sich eine Ausgabevoransicht, die neben der Ausgabe eines Beispielergebnisses der erstellten Abfrage auch prüft ob diese Funktionsfähig ist.

 Die rechte Spalte des Ausdruckseditor-Fensters zeigt jeweils eine Beschreibung der aktuell gewählten Funktion. Eine vollständige Liste mit Erläuterungen findet sich auch hier: http://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/expression.html

 .. image:: images/analyse/ausdruckseditor.jpg

 Die im Bild gezeigte Abfrage "*year( now() ) - to_int( "baujahr" ) > 50*" überprüft zum Beispiel anhand des **baujahr**-Feldes, ob das Objekt älter als 50 Jahre ist. Dazu wird das Jahr (*year( ... )*) aus der aktuellen Zeit (*now()*) extrahiert und davon die in **baujahr** eingetragene Jahreszahl abgezogen. Diese muss mithilfe von *to_int( ... )* zuerst in eine Ganzzahl umgewandelt werden, da es sich bei dem Feld um ein Textfeld handelt. Das Ergebnis wird anschließend darauf überprüft, ob es größer ist als 50. Das Endergebnis ist jeweils **0** für Objekte die 50 oder jünger sind, **1** für solche älter als 50 und Objekte, die keinen Eintrag in **baujahr** haben liefern das Ergebnis **NULL**, also einen Leerwert.

**Anwenden des Stils**

 Generell unterstützen alle Stilkategorien (Dropdown-Menü am oberen Rand des Fensters) Abhängigkeiten, da nahezu alle Eigenschaften der Grundlegenden Symbole (auf niedrigster Ebene) über Ausdrücke definiert werden können.

 Die Varianten **Kategorisiert** und **Abgestuft** bieten jedoch unmittelbarere Möglichkeiten, dies zu erreichen.

Kategorisiert

 .. image:: images/analyse/kategorisiert.png

 Wenn Sie die Option **Kategorisiert** wählen, sehen sie an oberster Stelle den Eintrag **Spalte**. Hierbei handelt es sich um das Bedingungsfeld. Sie können entweder über das Dropdownmenü eines der Felder dieses Layers direkt anwählen, in das Feld direkt Ihren Ausdruck eingeben oder über den Button rechts daneben den **Ausdruckseditor** öffnen.

 Darunter befinden sich die Einstellungen bezüglich des grundlegenden **Symbols**. Dies kann beliebig angepasst werden. Achten Sie jedoch darauf, dass dessen Farbe im Anschluss überschrieben wird.

 An dritter Stelle steht der Punkt **Farbverlauf**. Dieser bestimmt, welche Farben den einzelnen Kategorien zugeordnet werden. Sie können einen aus der Liste wählen oder ihn über die Schaltfläche **Bearbeiten** anpassen. Die Farben der einzelnen Kategorien werden dann gleichmäßig auf diesem Verlauf abgetragen. In den meisten Fällen reicht es vollkommen aus, diesen auf **Zufällige Farben** zu belassen.

 Das große Feld im Stileditor beinhaltet die einzelnen Kategorien, die sich aus der Abfrage aus **Spalte** ergeben. Mit einem Klick auf die Schaltfläche **Klassifizieren** wird für jeden eindeutigen Wert eine einzelne Kategorie erstellt, wie in der Abbildung oben für das Feld **rohrumhuellung**. Um nicht zu viele Kategorien zu erstellen eignet sich diese Variante am besten für Abfragen, die eine **begrenzte Menge an möglichen Werten** liefert.

 Erfasste Kategorien können mit einem Doppelklick auf ihr jeweiliges Symbol einzeln angepasst werden.

 In dem Beispiel oben wurden die verschiedenen **Rohrumhüllungen** der Hauptleitungen unterschiedlich eingefärbt. Daraus lässt sich sehr schnell ablesen, dass bei einem Großteil des Netzes die Umhülling **unermittelt** ist. Der Rest teilt sich nahezu vollständig zwischen **Kunststoff** und **gesintertem Polyethylen** auf.

Abgestuft

 .. image:: images/analyse/abgestuft.png

 In der Variante **Abgestuft** befinden sich auch wieder die Einträge **Spalte** und **Symbol**, die sich verhalten, wie bereits für **Kategorisiert** beschrieben.

 Das **Legendenformat** legt fest, wie die einzelnen Klassen in der Legende beschriftet werden. Standardmäßig werden der Minimalwert (*%1*) und Maximalwert (*%2*) mit Strich getrennt und mit einer Nachkommastelle (**Genauigkeit**) dargestellt.

 Bei der Option **Methode** können Sie wählen, auf welche Weise die Werte abgetragen werden sollen. **Color** stellt **Farbverläufe** zur Verfügung, die sich wie oben beschrieben anpassen lassen. **Size** erlaubt es eine Minimal- und Maximalgröße zu definieren.

 Auch hier dient das große Feld dazu, die einzelnen Klassen abzutragen. Jedoch werden diese in diesem Fall nicht nach eindeutigen Werten vergeben. Stattdessen wählen Sie rechts darunter wie viele einzelne Klassen sie dargestellt haben möchten und alle Elemente werden auf die Verteilt, was diese Variante sehr geeignet dazu macht, große Mengen verschiedener Zahlen abzutragen. Das Dropdownmenü **Modus** auf der linken Seite bestimmt, wie diese Verteilung stattfindet.

 - Die Standardoption **Gleiches Intervall** teilt die Klassen gleichmäßig zwischen höchstem und niedrigstem Wert auf.
 - **Quantil (Gleiche Anzahl)** dagegen definiert die einzelnen Klassen so, dass sich in jeder etwa gleich viele Elemente befinden.
 - **Natürliche Unterbrechungen (Jenks)** trennt an erkennbaren Lücken in der Werteverteilung.
 - **Standardabweichungen** geht vom Mittelwert aus und legt die Abweichung davon dar.
 - **Schöne Unterbrechungen** Setzt die Verteilung so, dass die Grenzpunkte auf "schönen" Werten liegen, etwa Vielfache von 2, 5 oder 10.

 **Hinweis**: Diese Version kann nur Zahlenwerte abtragen, da sich Texte nicht oder nur schwer in ein eindeutiges Spektrum einordnen lassen. Deshalb empfiehlt es sich darauf zu achten dass das Ergebnis der Abfrage eine Zahl ist oder sich mit *to_int( ... )* oder *to_real( ... )* in eine solche konvertieren lässt.

 Das oben gezeigte Beispiel färbt die Hauptleitungen abhängig von ihrem **Baujahr** ein. Wie bereits angesprochen muss das Feld zuerst zu einer Zahl konvertiert werden, weshalb sich in der Option **Spalte** der Ausdruck *to_int( "baujahr" )* befindet. Die jüngsten Leitungsabschnitte sind hier dunkelblau und die ältesten gelb gezeichnet. Durch die Verwendung der "**Gleiches Intervall**"-Verteilung kann man von den Farben direkt auf das ungefähre Baujahr schließen, sowie Muster im Ausbau des Netzes erkennen.

Regelbasierend

 Die Variante **Regelbasierend** ist die Version die momentan alle Layer des Demo-Projektes verwenden. Hier lassen sich verschiedene Symbole abhängig von diversen **Regeln** manuell einstellen. So kann automatisch zwischen Elementen mit bestimmten Eigenschaften unterschieden werden.

 Hier lassen sich schön einfache Hervorhebungen hinzufügen. Dazu klicken Sie auf auf den Button mit dem grünen **+**-Symbol links unter der Liste, um eine neue Darstellungsregel hinzuzufügen. In der Liste doppelklicken Sie auf den neuen Eintrag. Es öffnet sich ein Dialog in dem Sie die Gestaltung einstellen können. In diesem Dialog lässt sich auch die Bedingung definieren, bei der das Objekt angezeigt werden soll (zu finden an zweiter Stelle unter dem Punkt **Filter**). Hier können Sie Ihre Bedingung entweder direkt in das Textfeld eingeben oder mit dem Button mit er Aufschrift "**...**" den Ausdruckseditor öffnen.

 Die nachfolgende Grafik hebt bedingt durch die am Anfang erwähnte Abfrage "*year( now() ) - to_int( "baujahr" ) > 50*" alle Leitungsabschnitte rot hervor, die älter sind als 50 Jahre:

 .. image:: images/analyse/einfaerbung.jpg

 Damit diese neuen Darstellungen sichtbar sind, muss darauf geachtet werden, dass sie an oberster Stelle gerendert werden. Ansonsten könnten andere Symbole auf der Ebene sie überdecken. Dafür wählen Sie im Stileditor den Button **Symbolebenen...** rechts unter der Liste. Es öffnet sich ein Fenster in dem Sie Ihre neue Darstellungsregel auswählen und ihr eine höhere Priorität zuordnen als die anderen besitzen (im Beispiel der Wert *2*).

 .. image:: images/analyse/symbolebenen.jpg

**HINWEIS**

 Es empfiehlt sich vor der Änderung des Stils den Layer zu duplizieren (**Rechtsklick > Duplizieren**). Angewendete Änderungen im Stil **überschreiben** den alten Wert. Bei einem Speichervorgang des Gesamtprojektes würden diese dann auch in der Projektdatei überschrieben werden und sind danach nicht wiederherstellbar.

 Weitere Details finden sich auch in der QGIS Dokumentation: https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html#style-properties


Das Verarbeitungswerkzeuge-Fenster
----------------------------------

**Übersicht**

 Das **Verarbeitungswerkzeuge**-Fenster, auch **Werkzeugkiste** genannt, stellt eine umfangreiche Sammlung von Werkzeugen bereit. Es lässt sich über das Menü **Verarbeitung > Werkzeugkiste** oder die Tastenkombination **Strg+Alt+T** aufrufen. Sollte dieses Menü nicht existieren, muss es zuerst aktiviert werden. Öffnen Sie dazu **Erweiterungen > Erweiterungen verwalten und installieren...** und setzen Sie den Haken vor der Erweiterung **Processing**. Danach können Sie die Werkzeugkiste wie beschrieben anwählen.

 .. image:: images/analyse/werkzeugkiste.png

 Es öffnet sich ein Fenster das alle verfügbaren Werkzeuge nach Anbieter und Kategorien geordnet auflistet. Für den einfachen Zugriff befindet sich am oberen Rand eine Suchleiste, die die angezeigten Elemente filtert. Viele sind sehr spezifisch und für dieses Modell nicht von nutzen, doch besonders die Allgemeineren sind sehr hilfreich. So lassen sich etwa unter **QGIS-Geo-Algorithmen > Vektoranalysewerkzeuge** die Optionen **Punkte in Polygon zählen** und **Linienlängen summieren** finden, die sich entsprechend dafür eignen beispielsweise die Anzahl von Hausanschlüssen bzw. Anzahl und Länge von Anschlussleitungen in einem bestimmeten Gebiet zu bestimmen. Die **Puffer**-Werkzeuge aus **QGIS-Geo-Algorithmen > Vektorgeometriewerkzeuge** sind hilfreich für Abstandsbeziehungen und können für komplexere Anforderungen mit den Verschneidungswerkzeugen aus **QGIS-Geo-Algorithmen > Vektorlayerüberlagerungswerkzeuge** kombiniert werden. In letzterem findet sich auch das **Linienschnittpunkte**-Werkzeug, das es erlaubt - wie der Name sagt - Schnittpunkte zwischen den Linien zweier Layer (oder eines Layers mit sich selbst) zu finden.

**Werkzeuge**

 Abgesehen von ein paar speziellen Ausnahmen sind alle Werkzeuge weitgehend gleich aufgebaut. Unten ist das Beispiel von **Linienlängen summieren** dargestellt. Der obere Teil wird von den Argumenten eingenommen, die das Werkzeug zur Durchführung benötigt. Diese sind abhängig von dem einzelnen Werkzeug; zumeist handelt es sich um ein oder mehrere Eingabe-Layer und verschiedene Werte wie Zahlenwerte (z.B. für Abstände) und/oder Auswahlmenüs. In diesem Fall handelt es sich um den Linien-Layer, den Polygon-Layer in den diese verrechnet werden sollen, sowie die Benennung der Felder für die errechnete Länge und Anzahl der Linien.

 Wenn auf den gewählten Eingabe-Layern Auswahlen existieren, wird der Vorgang auf diese beschränkt.

 Das unterste Textfeld legt den Dateipfad fest, unter dem der durch dieses Werkzeug erzeugte Layer gespeichert werden soll. Der Ort und andere Details können über den Button rechts davon eingestellt werden. Ist kein Speicherort gewählt, wird stattdessen ein **Temporärlayer** erzeugt. Dieser verhält sich wie ein normaler Layer - mit dem Unterschied dass er am Ende der Sitzung nicht gespeichert wird und verfällt. Dies bietet sich für temporäre Berechnungen sowie Zwischenschritte an, die später nicht mehr benötigt werden. Sollten Sie einen als temporär generierten Layer nachträglich doch speichern wollen, lässt sich dies über einen **Rechtsklick** auf den entsprechenden Layer-Eintrag **> Speichern als...** erreichen. Unter dem Layer-Textfeld befindet sich die Option "**Öffne Ausgabedatei nach erfolgreicher Ausführung**". Wenn aktiv wird das Ergebnis automatisch als neuer Layer eingefügt.

 Die rechte Seite des Fensters wird zumeist von einer Beschreibung eingenommen, welche die Funktion des Werkzeuges genauer darlegt.

 .. image:: images/analyse/linienlaengen.png

 Die Ergebnis-Layer können selbstverständlich wie oben dargelegt über den Stil grafisch Ausgewertet werden. Nachfolgend sehen Sie die **summierten Längen** der **Anschlussleitungen** auf einem Polygongitter mit einer Kantenlänge von 500 Metern abgetragen. Zuerst wurde das Gitter mithilfe des Werkzeuges **Gitter erzeugen** über die gesamte Fläche die **Anschlussleitungen** enthält erstellt und darauf über **Linien Summieren** die Leitungen darin verrechnet. Ein **abgestufter** Stil zeigt grafisch, wie dicht die Leitungen in diesen 2.500 m² jeweils liegen.

 .. image:: images/analyse/laengenraster.png

 Eine ausführliche Liste über die verfügbaren Werkzeuge sowie Informationen über deren Aufruf per Code finden Sie hier: https://docs.qgis.org/2.18/en/docs/user_manual/processing_algs/index.html


Erweiterungen
-------------

 Es gibt einige Erweiterungen die weitere nützliche Funktionen zu QGIS hinzufügen.

**Straßengraph-Erweiterung**

 Zwar ist dieses Plugin hauptsächlich auf Straßen ausgelegt, doch stellt es doch zuverlässig die kürzeste Strecke dar und ist zudem bereits in QGIS enthalten. Um es zu nutzen muss lediglich unter **Erweiterungen > Erweiterungen verwalten und installieren...** das Plugin **Straßengraph-Erweiterung** aktiviert werden. Das Plugin-Fenster lässt sich über **Ansicht > Bedienfelder > Kürzester Weg** öffnen.

 .. image:: images/analyse/kuerzester_weg.png

 Zu beachten ist hier, dass der Layer der analysiert wird nicht im eigentlichen Plugin-Fenster, sondern in einem separaten Menü ausgewählt wird. Dieses erreicht man über **Vektor > Straßengraph > Einstellungen**. Die meisten der Einstellungsmöglichkeiten sind rein für die Verwendung an Straßen nützlich. Der Punkt von Interesse ist die Option **Layer**.

 Wenn der Layer gesetzt ist, können vom Plugin-Fenster aus Start- und Endpunkt gesetzt werden. Dazu wählen Sie den Button neben der entsprechenden Zeile an und klicken an die entsprechende Stelle in ihrem Modell. Sind beide Punkte gesetzt, kann dieser Vorgang über den Button **Berechnen** gestartet werden. Das entsprechend gekennzeichnete Textfeld gibt daraufhin die Gesamtlänge dieser Strecke aus und der sich ergebene Pfad wird auf dem Modell hervorgehoben. Dieser kann anschließend mit der Schaltfläche **Exportieren** als eigener Layer gespeichert werden. **Löschen** entfernt alle Eingaben und Ergebnisse aus dem Fenster und beendet die Hervorhebung.

**Heatmap**

 QGIS besitzt zwar eine interne Variante des Stils welche dynamisch Heatmaps darstellt, doch ist diese sehr rechenaufwändig und liefert keinerlei Werte für Berechnungen. Diese Schwächen kann man mithilfe des Heatmap-Plugins umgehen. Installiert wird es wie gewohnt über **Erweiterungen > Erweiterungen verwalten und installieren...**. Daraufhin können Sie es unter **Raster > Heatmap > Heatmap...** aufrufen.

 .. image:: images/analyse/heatmap.png

 Die erzeugte Heatmap wird als Raster gespeichert. Dazu müssen Sie unter **Ausgabe** einen Dateipfad angeben. Darunter wählen Sie den Dateityp. **Radius** bezieht sich auf die Fläche, die von jedem Punkt auf der Heatmap beeinflusst wird.

 In den **Erweiterten Einstellungen** gibt es zusätzliche Optionen. So können Sie zum Beispiel die Auflösung der Heatmap bestimmen oder die Größe/Gewichtung einzelnen Elemente über Felder festlegen.

**Räumliche Abfrage**

 Die **Räumliche Abfrageerweiterung** bietet die Möglichkeit, Objekte im Modell zu suchen, die in bestimmten geometrischen Zusammenhängen zueinander stehen und eine Auswahl aus diesen zu erstellen. Installiert wird sie wie gewohnt in **Erweiterungen > Erweiterungen verwalten und installieren...**. Sie starten es über **Vektor > Räumliche Abfrage > Räumliche Abfrage**.

 .. image:: images/analyse/abfrage.png

 Hier wählen Sie den **Quelllayer**, in dem sie die Auswahl treffen möchten. Unter diesem befindet sich ein Auswahlmenü, in welcher **geometrischen Beziehung** sich dessen Objekte zu denen des **Referenzlayers** befinden sollen, den Sie darunter wälen können. Dieses bietet unterschiedliche Optionen, je nachdem von welchem Typ (Punkt, Linie, Ploygon) die beiden Layer sind. Beide Layer bieten die Möglichkeit nur ausgewählte Objekte zu berücksichtigen. Sollten Sie auf dem **Quellayer** Auswahlen haben können Sie anschließend noch wählen ob diese um die Ergebnisse erweitert oder verringert werden soll oder ob Sie eine ganz neue Auswahl erstellen möchten. Die Schaltfläche **Anwenden** startet die Abfrage.
