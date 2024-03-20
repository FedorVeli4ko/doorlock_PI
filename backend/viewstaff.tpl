 <!DOCTYPE html>

<html>

<head>
		
	<p>Сейчас в кабинете:</p>
	<table border="1">
		%for row in plist:
		<tr>
			%for col in row:
			<td>{{col}}</td>
			%end
		</tr>
		%end
		</table>

</body>



</html>
