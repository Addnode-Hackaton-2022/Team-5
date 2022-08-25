# Instruktioner
- Installera Rpanion 0.8
- Modifiera filen /home/pi/Rpanion-server/python/rtsp-server.py - ett exempel finns under instructions-mappen
  På raderna som börjar med pipeline_str har vi lagt till "config-interval=1" på rtph264pay så att
	! rtph264pay name=pay0 pt=96
	blir
	! rtph264pay name=pay0 pt=96 config-interval=1	
- Ställ in Rpanion enligt bilderna i instructions-mappen


* Välj en teamleader för erat team.
  - Teamleader - Victor Blomberg
* Välj ett namn för erat team. Detta skall även skrivas på dörren.
  - Namn - Pajkastarna
* Vilken utmaning jobbar ni med?
  - Namn - Korrekt strömning från drönare
 

### Övergripande beskrivning och val av utmaning
Korrekt strömning från drönare

### Team

#### Namn på medlemmar 
* Victor Blomberg
* Scott Levkowetz
* Fredrik Lemón Larsson
* Marcus Johansson
* Victor Böhmer
* Rasmus Jansson

#### Hur har ni jobbat inom teamet? Har alla gjort samma eller har ni haft olika roller?
Vi har delat upp arbetet utefter vilka uppgifter och utmaningar som har uppenbarat sig.

### Teknik. Beskrivningen på eran teknikstack, språk och APIer ni har använt.
Python, C#

### Lösning, dessa frågor ska minst besvaras
 * Hur har ni löst utmaningen?
Vi har med hjälp av ett python-script plockat ut den telemetridata som är relevant för videostabiliseringen.
Skriptet kombinerar sedan datan med videoströmmen och skickar vidare TCP-paket.
För att bevisa att det fungerar har vi även utvecklat en mottagare i .NET som kan ta emot strömmen som både består av video och telemetidata.

 * Hur långt har ni kommit?
 Vi är klara, men det är inte den lösning vi hade önskat oss allra helst.
 
 * Vad är nästa steg?
Nästa steg är att med hjälp av lösningen kunna ta hand om telemetridatat för att bildstabilisera videon.
 
 * Några rekommendationer för framtiden?
Titta på drönartillverkaren Parrots lösningar som verkar göra ungefär det vi vill.
https://github.com/Parrot-Developers/libvideo-streaming
Beskrivning: https://developer.parrot.com/docs/pdraw/video-metadata.html#frame-metadata
 
 * Några insikter, begränsningar eller utmaningar ni stött på som är intressanta att dela med der av?
 - Telemetridatan som genereras av Rpanion sker bara en gång per sekund vilket kanske inte är tillräckligt för att kunna använda som underlag vid bildstabilisering.
 - En hel del tid har gått åt till att undersöka möjligheterna att lägga till telemetridatat i videoströmmens RTP-header - ett spår som vi till slut fick överge.
 - Vi är osäkra på hur väl videoströmmen och telemetridatan synkar med varandra och har inte haft tid att undersöka det vidare.


