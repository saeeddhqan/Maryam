$(document).ready(function(e) {   
    var workspace = document.getElementById("workspace").value;
    getSummary(workspace);
    getModules(workspace);
 });

//Summary
var summary; // saving data from workspace in summary globally
var options; //Module options

function showModules(){
	$('#module option:not(:first)').remove();
	var data = summary;
	var selected = document.getElementById('type').value;
	console.log(selected);
	for(module in data){
		if(data[module].split('/')[0] === selected){
			var opt = document.createElement('option');
			opt.innerText = data[module].split('/')[1];
			opt.value = data[module].split('/')[1];
			document.getElementById('module').appendChild(opt);
		}
	}
}

function showOptions(){
	$('#module__options').remove();
	var selected = document.getElementById('module').value;
	var mod_opt = options[selected]['options'];
	console.log(mod_opt);
	var table = document.getElementById('dataTable');
	var row = table.insertRow(-1);
	row.className="table__row";
	row.id = 'module__options';


	//Options
	var opt_cell = row.insertCell(-1);
	opt_cell.innerHTML = `<ul><b>Options:</b></ul>`;
	opt_cell.id = 'opt_cell';
	for(option in mod_opt){
		var opt = document.createElement('p');
		if(mod_opt[option][0] != 'output'){
			if(mod_opt[option][5] === 'store'){
				if(mod_opt[option][2]=='true'){
					opt.innerHTML = `<a><label><b>${mod_opt[option][0]}</b></label><input id=${option} class = ${mod_opt[option][0]} type = 'text' value =${mod_opt[option][1]} required ></input></a>`;
				}
				else{
					opt.innerHTML = `<a><label><b>${mod_opt[option][0]}</b></label><input id =${option} class = ${mod_opt[option][0]} type = 'text' value =${mod_opt[option][1]} ></input></a>`;
				}
			}
			else{
				if(mod_opt[option][2] === 'true'){
					opt.innerHTML = `<a><label><b>${mod_opt[option][0]}<b></lable><input checked class = ${mod_opt[option][0]} type='checkbox' value=${mod_opt[option][1]} 
					onclick="this.value === 'true' ? this.value = 'false' : this.value = 'true' "></input></a>`;
				}
				else{
					opt.innerHTML = `<a><label><b>${mod_opt[option][0]}</b></lable><input class = ${mod_opt[option][0]} type='checkbox' value=${mod_opt[option][1]} 
					onclick="this.value === 'true' ? this.value = 'false' : this.value = 'true' "></input></a>`;
				}
			}
			opt_cell.appendChild(opt);
		}
	}

	//Description
	var desc_cell = row.insertCell(-1);
	desc_cell.id = 'module__desc';
	desc_cell.innerHTML = `<ul><b>Description:</b></ul>`;

	var name = document.createElement('p');
	name.innerHTML = `<b>Name: </b><a>${options[selected]['name']}</a>`;
	document.getElementById('module__desc').append(name);

	var author = document.createElement('p');
	author.innerHTML = `<b>Author: </b><a>${options[selected]['author']}</a>`;
	document.getElementById('module__desc').append(author);

	var version = document.createElement('p');
	version.innerHTML = `<b>Version: </b><a>${options[selected]['version']}</a>`;
	document.getElementById('module__desc').append(version);

	var desc = document.createElement('p');
	desc.innerHTML = `<b>Description: </b><a>${options[selected]['description']}</a>`;
	document.getElementById('module__desc').append(desc);

	//Sources
	var sources_cell = row.insertCell(-1);
	sources_cell.id = 'module__sources';
	sources_cell.innerHTML = `<ul><b>Sources</b></ul>`;
	var sources = options[selected]['sources'];
	for(source in sources){
		var mod_source = document.createElement('p');
		mod_source.innerText = sources[source];
		sources_cell.append(mod_source);
	}

	//Examples
	var examples_cell = row.insertCell(-1);
	examples_cell.id = 'module__examples';
	examples_cell.innerHTML = `<ul><b>Examples</b></ul>`;
	var examples = options[selected]['examples'];
	for(example in examples){
		var mod_example = document.createElement('p');
		mod_example.innerText = examples[example];
		examples_cell.append(mod_example);
	}

}

async function runCommand(){
	$('#reload').remove();
	var reload = document.createElement("a");
	reload.innerHTML = `<a id = "reload" style="font-size:110%; padding: 5px;" data-toggle="tooltip" data-placement="top" title="Reload" onclick="displayData(summary)">↺</a>` ;
	$('#dataTable tr:first th:last').append(reload) ;
	var command = '';
	var selected = document.getElementById('module').value;
	var mod_opt = options[selected]['options'];
	command += selected;
	for(opt in mod_opt){
		if(mod_opt[opt][0] === 'output'){
			command+=' --output';
		}
		else{
			try{
				var opt_value = document.getElementsByClassName(mod_opt[opt][0])[0].value;
				if(opt_value === 'false' || opt_value === 'null'){
					continue;
				}
				if(opt_value === 'true'){
					command += ' ';
					command += mod_opt[opt][4];
				}
				else{
					command += ' ';
					command += mod_opt[opt][4];
					command += ' ';
					command += opt_value;
					console.log(opt_value);
				}
			}
			catch(err){
				console.log(err);
			}
		}
	}
	await fetch('/api/run/',{
		method: 'POST',
		headers: {
			'Content-type': 'application/json'
		},
		body: JSON.stringify({
			'cmd': command
		})
	})
	.then(function (response) {
		if (response.ok) {
			return response.json();
		}
		return Promise.reject(response);
	}).then(function (data) {
		var outputs = data.output;
		document.getElementById('output').innerHTML = `<ul class="output" id = "outputs" onclick="this.style.height==='100%' ? this.style.height='40px' : this.style.height='100%'"><a data-toggle="tooltip" data-placement="bottom" title="Expand" onclick="this.innerText ==='▼' ? this.innerText='▲' : this.innerText='▼'">▼</a></ul>`;
		for(output in outputs){
			if(typeof outputs[output] === 'object' && outputs[output].constructor === Object){
				for(info in outputs[output]){
					var dict = outputs[output][info];
					while(Array.isArray(dict)){
						dict = dict[Object.key(dict)[0]];
					}
					var out = document.createElement('li');
					console.log(dict[info]);
					out.innerText = dict[info];
					document.getElementById('outputs').appendChild(out);
				}
			}
			else{
				console.log(outputs[output]);
				var out = document.createElement('li');
				out.innerText = outputs[output];
				document.getElementById('outputs').appendChild(out);
			}
		}

	}).catch(function (error) {
		console.warn('Something went wrong.', error);
	});
}


function displayData(data){
	$('#reload').remove();
	$('#dataTable tr:not(:first)').remove();
	var table = document.getElementById('dataTable');
	var row = table.insertRow(-1);
	row.className="table__row";
	var type = row.insertCell(-1);
	type.className = "table__data";
	type.innerHTML = `<select class="form-control" id = "type" onchange="showModules()"><option selected disabled>Select Target</option></select>`;
	var mod = row.insertCell(-1);
	mod.className = "table__data";
	mod.innerHTML = `<select class="form-control" id = "module" onchange = "showOptions()"><option selected disabled>Select Target</option></select>`;
	var target = row.insertCell(-1);
	target.className = "table__data";
	target.innerHTML = `<input class="form-control" id = "target" onchange="document.getElementById(0).value = this.value" required></input>`;
	var result = row.insertCell(-1);
	result.className = "table__data";
	result.id = "output";
	result.innerHTML = `<button type="button" class="btn btn-primary" id = "result" onclick = "runCommand()">Get Result</button>`;
	const types = new Set();
	for (module in data){
		if(!(types.has(data[module].split('/')[0]))){
			types.add(data[module].split('/')[0]);
			var opt = document.createElement('option');
			opt.innerText = data[module].split('/')[0];
			opt.value = data[module].split('/')[0];
			document.getElementById('type').appendChild(opt);
		}
	}
	console.log(data);
}

function getModules(workspace){
	$("#dataTable tr:not(:first)").remove();
	fetch('/api/run/',{
		method: 'GET',
		headers: {
			'Content-type': 'application/json'
		}
	})
	.then(function (response) {
		if (response.ok) {
			return response.json();
		}
		return Promise.reject(response);
	}).then(function (data) {
		displayData(data.modules);
		summary = data.modules;
		options = data.meta;
		console.log(options);
	}).catch(function (error) {
		console.warn('Something went wrong.', error);
	});
}

function getSummary(workspace){
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
	}).catch(function (error) {
		console.warn('Something went wrong.', error);
	});
}