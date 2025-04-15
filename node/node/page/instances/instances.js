frappe.pages['instances'].on_page_load = function (wrapper) {
	// Inject styles
	$(`<style>
		#region-grid, #iso-grid, #node-grid, #server-grid, #vm-grid {
			display: grid;
			grid-template-columns: repeat(4, minmax(0, 1fr));
			gap: 1rem;
			margin-bottom: 2rem;
		}
		.region-card, .iso-card, .node-card, .server-card, .vm-card {
			background: #fff;
			border: 1px solid #e2e8f0;
			border-radius: 0.5rem;
			padding: 1rem;
			box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
			transition: border 0.2s ease;
			cursor: pointer;
		}
		.region-card:hover, .iso-card:hover, .node-card:hover, .server-card:hover, .vm-card:hover {
			border-color: #3b82f6;
		}
		.card-title {
			font-weight: 600;
			font-size: 0.95rem;
			margin-bottom: 0.25rem;
		}
		.card-subtitle {
			font-size: 0.75rem;
			color: #6b7280;
		}
		.tab-button {
			padding: 0.5rem 1.25rem;
			border-radius: 0.375rem;
			border: 1px solid #e5e7eb;
			background-color: #f9fafb;
			color: #374151;
			transition: all 0.2s ease;
			font-size: 0.875rem;
		}
		.tab-button:hover {
			background-color: #e5e7eb;
		}
		.tab-button.active-tab {
			background-color: #3b82f6;
			color: white;
			border-color: #3b82f6;
		}
		h3.section-heading {
			font-size: 1.125rem;
			font-weight: 600;
			margin-bottom: 1rem;
		}
	</style>`).appendTo('head');

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Instance',
		single_column: true
	});
	const container = $('<div class="p-6 space-y-6">').appendTo(page.body);

	// Region heading
	$('<h2 class="text-xl font-bold">Region</h2>').appendTo(container);

	// Continent filter buttons
	const tab_wrapper = $(`
		<div class="flex gap-3 border-b pb-2 mb-4 text-sm font-medium">
			<button class="tab-button active-tab" data-continent="All">All</button>
			<button class="tab-button" data-continent="Europe">Europe</button>
			<button class="tab-button" data-continent="Asia">Asia</button>
			<button class="tab-button" data-continent="Africa">Africa</button>
			<button class="tab-button" data-continent="Americas">Americas</button>
			<button class="tab-button" data-continent="Oceania">Oceania</button>
		</div>
	`).appendTo(container);

	const region_grid = $('<div id="region-grid">').appendTo(container);

	let allRegions = []; // store all for filtering

	frappe.call({
		method: "node.node.doctype.region.region.get_all_regions",
		callback: function (r) {
			allRegions = (r.message || []).slice(0, 43); // limit to 43
			// allRegions = r.message || [];
			render_regions(region_grid, allRegions); // default

			tab_wrapper.find('.tab-button').on('click', function () {
				tab_wrapper.find('.tab-button').removeClass('active-tab');
				$(this).addClass('active-tab');

				const continent = $(this).data('continent');
				const filtered = continent === 'All'
					? allRegions
					: allRegions.filter(r => r.continent === continent);

				render_regions(region_grid, filtered);
			});
		}
	});

	// ISO section
	const iso_section = $('<div id="iso-section">').appendTo(container);
	$('<h3 class="section-heading">ISO Images</h3>').appendTo(iso_section);
	const iso_grid = $('<div id="iso-grid">').appendTo(iso_section);
	load_data('ISO Images', ['name', 'iso_image'], iso_grid, 'iso');

	// Node section
	const node_section = $('<div id="node-section">').appendTo(container);
	$('<h3 class="section-heading">Nodes</h3>').appendTo(node_section);
	const node_grid = $('<div id="node-grid">').appendTo(node_section);
	load_data('Node', ['name', 'status'], node_grid, 'node');

	// Server List
	const server_section = $('<div id="server-section">').appendTo(container);
	$('<h3 class="section-heading">Servers</h3>').appendTo(server_section);
	const server_grid = $('<div id="server-grid">').appendTo(server_section);
	load_data('Server List', ['name', 'port', 'user_name', 'status'], server_grid, 'server');

	// Virtual Machines
	const vm_section = $('<div id="vm-section">').appendTo(container);
	$('<h3 class="section-heading">Virtual Machines</h3>').appendTo(vm_section);
	const vm_grid = $('<div id="vm-grid">').appendTo(vm_section);
	load_data('Virtual Machine', ['name'], vm_grid, 'vm');
};

// Render region cards
function render_regions(wrapper, regions) {
	wrapper.empty();
	regions.forEach(region => {
		const flagTag = region.flag
			? `<img src="${region.flag}" class="flag-img" alt="Flag"/>`
			: '🌐';

		const card = $(`
			<div class="region-card">
				<div class="card-title">${flagTag} ${region.region_name}</div>
				<div class="card-subtitle">${region.continent}</div>
			</div>
		`);
		wrapper.append(card);
	});
}


// Reusable data loader
function load_data(doctype, fields, wrapper, type) {
	frappe.call({
		method: "frappe.client.get_list",
		args: {
			doctype,
			fields,
			limit_page_length: 100
		},
		callback: function (r) {
			const data = r.message || [];
			wrapper.empty();

			if (!data.length) {
				wrapper.append(`<div class="text-sm text-gray-500 col-span-full">No ${type} records found.</div>`);
				return;
			}

			data.forEach(item => {
				const title = item[fields[1]] || item.name;
				const subtitle = item.status || type.toUpperCase();
				const card = $(`
					<div class="${type}-card">
						<div class="card-title">${title}</div>
						<div class="card-subtitle">${subtitle}</div>
					</div>
				`);
				wrapper.append(card);
			});
		}
	});
}
