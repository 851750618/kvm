function validate(obj) {
	var ok = true;
	var info = [];
	for(var k in obj) {
		var v = obj[k];
		var num = parseInt($(k).val());
		if(typeof(v) == 'string' && $(k).val() != $(v).val()) {
			$(k).parent('div').addClass('has-error');
			$(v).parent('div').addClass('has-error');
			ok = false;
		} else if(v instanceof Array && (isNaN(num) || num < v[0] || num > v[1])) {
			$(k).parent('div').addClass('has-error');
			info.push($(k).attr('placeholder'));
			ok = false;
		} else if(!(v instanceof Array) && typeof(v) != 'string' && !$(k).val().match(v)) {
			$(k).parent('div').addClass('has-error');
			info.push($(k).attr('placeholder'));
			ok = false;
		} else {
			$(k).parent('div').removeClass('has-error');
		}
	}
	info.length && alert(info.join('\n'));
	return ok;
}

$(document).ready(function() {
	$('.fa-download').each(function() {
		var o = $(this);
		var url = o.parent().attr('href');
		url = url.substr(url.lastIndexOf('/') + 1);
		o.parent().attr('download', url);
	});
});