$(document).ready(function(e) {   
    var workspace = document.getElementById("workspace").value;
    getSummary(workspace);
 });


//Summary
var summary; // saving data from workspace in summary globally

function outputData(module){
	document.getElementById(`row-${module}`).deleteCell(-1);
	var data = summary;
	var selected = document.getElementById(`target-${module}`).value;
	var output = document.getElementById(`row-${module}`).insertCell(-1);
	output.className = "table__data";
	output.innerHTML = `<ul class="output" id = "output-${module}-${selected}" onclick="this.style.height==='100%' ? this.style.height='40px' : this.style.height='100%'"><a data-toggle="tooltip" data-placement="bottom" title="Expand" onclick="this.innerText ==='▼' ? this.innerText='▲' : this.innerText='▼'">▼</a></ul>`
	var expression = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi;
	var regex = new RegExp(expression);
	for(result in data[module][selected]){
		if(Array.isArray(data[module][selected][result])){
			for(info in data[module][selected][result]){
				var out = document.createElement('li');
				url = `${data[module][selected][result][info]}`
				if(url.match(regex)){
					out.innerHTML = `<a href="${data[module][selected][result][info]}">${data[module][selected][result][info]}</a>`
				}
				else{
					out.innerHTML = `<a href="#">${data[module][selected][result][info]}</a>`
				}
				out.value = result;
				document.getElementById(`output-${module}-${selected}`).appendChild(out);
			}
		}
		else{
			var out = document.createElement('li');
			url = `${data[module][selected][result]}`
			if(url.match(regex)){
				out.innerHTML = `<a href="${data[module][selected][result]}">${data[module][selected][result]}</a>`
			}
			else{
				out.innerHTML = `<a href="#">${data[module][selected][result]}</a>`
			}
			out.value = result;
			document.getElementById(`output-${module}-${selected}`).appendChild(out);
		}
	}
}


function displayData(data){
	var table = document.getElementById('dataTable');
	for (module in data){
		var row = table.insertRow(-1);
		row.className="table__row";
		row.id = `row-${module}`
		var type = row.insertCell(-1);
		type.className = "table__data";
		type.innerText = module.split('/')[0];
		var mod = row.insertCell(-1);
		mod.className = "table__data"
		mod.innerText = module.split('/')[1];
		var target = row.insertCell(-1);
		target.className = "table__data";
		row.insertCell(-1);
		target.innerHTML = `<select class="targets" id = "target-${module}" onchange="outputData('${module}')"><option selected disabled>Select Target</option></select>`;
		for (targets in data[module]){
			var opt = document.createElement('option');
			opt.innerText = targets;
			opt.value = targets;
			document.getElementById(`target-${module}`).appendChild(opt);
		}
	}
	console.log(data);
}

function getSummary(workspace){
	$("#dataTable tr:not(:first)").remove();
	fetch('/api/workspaces/',{
		method: 'POST',
		headers: {
			'Content-type': 'application/json'
		},
		body: JSON.stringify({
			'workspace': workspace
		})
	})
	.then(function (response) {
		if (response.ok) {
			return response.json();
		}
		return Promise.reject(response);
	}).then(function (data) {
		displayData(data);
		summary = data;
	}).catch(function (error) {
		console.warn('Something went wrong.', error);
	});
}

