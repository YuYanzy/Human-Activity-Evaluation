#coding=utf-8
from FlaskApp import app

@app.route('/')
def index():
     html = """<h1>Velkommen til Road2zero-API!</h1>
     <p>Road2zero er et studentprosjekt og lekegrind for geomatikkstudentene Joakim Husefest, Stian Rostad og Eirik Aabøe på NMBU<br>
     Appen er ment til å detektere brukerens aktivitet på kollektivtransport automatisk ved hjelp av postgis og åpne data.</p>
     <p>Vår database inneholder jernbanestasjoner, busstasjoner og trikkestopp i Norge.<br>
     Av linjedata består databasen av  jernbane-, t-bane og trikkelinjer </p>
     <p> Vi utvikler appen for android og ios med React-Native.
     <table>
     <tr>
     Her er detaljert informasjon om hvordan vi bruker api-et per idag: </p>
     <h2> Buss-api  </h2>
     <th> <a href="http://188.166.168.99/buss/?lon=10.7878691&lat=59.662123">http://188.166.168.99/buss/?lon=10.7878691&lat=59.662123</a> </th>
     <p> Returnerer distanse til nærmeste busstopp i første parameter. I andre parameter returneres True eller False på om brukeren er <br>
	nærmere busstopp enn 15m. Postgis funksjonen er st_Dwithin. Vi har lagt på en buffer på 5 meter. Tredje parameter er hvilken type Stasjon.</p>
	</table>

     <h2> Tog-api  </h2>
	<p> Returnerer distanse til nærmeste toglinje i første parameter. Returnerer True eller False om brukeren er innenfor en avstand fra toglinjen<br>
	med en en buffer på 5 meter </p>
	<th> <a href="http://188.166.168.99/tog/?lon=10.7878691&lat=59.662123">http://188.166.168.99/tog/?lon=10.7878691&lat=59.662123</a> </th>
	
	<h2> Busstopp-api </h2>
	<p> Returnerer 5 nærmeste busstopp med tilhørende koordinater og busstoppets navn </p>
	<th> <a href="http://188.166.168.99/scoords/?lon=10.7878691&lat=59.662123">http://188.166.168.99/scoords/?lon=10.7878691&lat=59.662123</a> </th>     
</tr>
	

     """
     return html
