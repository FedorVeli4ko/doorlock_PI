 <!DOCTYPE html>

<html>

<head>
	<title>Работа с пользователями</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8">
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
</head>

<body>
	<form action="/staff" method="post" enctype="multipart/form-data">
		<h1>
		Добавить запись в базу:
		</h1>
		
		<p>
		Имя Отчество:<br> 
		<input id="name" name="staff_name" type="text" size="50">
		</p>
		
		<p>
		Фамилия:<br> 
		<input id="surname" name="staff_surname" type="text" size="50">
		</p>
		
		<p>
		Класс:<br> 
		<input id="class" name="staff_class" type="text" size="3">
		</p>
		
		<p>
		Учитель?<br>
		Да <input name="is_teacher" type="radio" value="yes">
		Нет <input name="is_teacher" type="radio" value="no" checked>
		</p>
		
		<p>
		<input name="OK" type="submit" value="Отправить запись в базу">
		</p>
	</form>
	
	<p>Список пользователей:</p>
	<table border="1">
		%for row in plist:
		<tr>
			%for col in row:
			<td>{{col}}</td>
			%end
			<td><a href="/images/{{row[0]}}.jpg"> Скачать код</a></td>
		</tr>
		%end
		</table>

</body>



</html>
