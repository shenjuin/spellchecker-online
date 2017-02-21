<!doctype html>
<head>
<title>Spell Checker</title>
<script type="text/javascript"
  src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript">
  var $SCRIPT_ROOT = "{{ request.script_name }}";
</script>
</head>

<body>
<script type="text/javascript">
  $(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + 'check', {
        word: $('input[name="word"]').val()
      }, function(data) {
        $('#result').text(data.result);
        $('input[name=word]').focus().select();
      });
      return false;
    };

    $('input[name=check]').bind('click', submit_form);
  });
</script>

<p>Enter a word to check its spelling:</p>
<p>
	<input name="word" type="text">
	<input name="check" value="Check" type="submit" />
</p>
<p>
	<span id="result"></span>
</p>
</body>
</html>