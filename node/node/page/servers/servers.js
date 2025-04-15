frappe.pages['servers'].on_page_load = function(wrapper) {
	// Inject custom flag style
	$(`<style>
		.flag-img {
			width: 24px;
			height: 16px;
			object-fit: cover;
			border: 1px solid #ccc;
			border-radius: 3px;
			margin-right: 6px;
			box-shadow: 0 1px 2px rgba(0,0,0,0.05);
		}
	</style>`).appendTo('head');

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Server List',
		single_column: true
	});

	const container = $(`
		<div class="p-6">
			<div class="flex justify-between items-center mb-4">
				<h2 class="text-lg font-bold">Instances</h2>
				<button class="btn btn-primary" id="add-server">+ Add</button>
			</div>
			<table class="table table-bordered w-full text-sm">
				<thead>
					<tr class="bg-gray-100 text-left">
						<th class="py-2 px-4">Server</th>
						<th class="py-2 px-4">Location</th>
						<th class="py-2 px-4">IP Address</th>
						<th class="py-2 px-4">Status</th>
						<th class="py-2 px-4">Operation</th>
					</tr>
				</thead>
				<tbody id="server-table-body"></tbody>
			</table>
		</div>
	`).appendTo(page.body);

	// Fetch servers with region and flag
	frappe.call({
		method: "node.node.doctype.server_list.server_list.get_servers_with_region_flags",
		callback: function(r) {
			const rows = r.message || [];
			const tbody = container.find("#server-table-body");
			tbody.empty();

			rows.forEach(server => {
				const flagImg = server.flag 
					? `<img src="${server.flag}" class="flag-img" alt="Flag of ${server.region}" />`
					: '🌐';

				const row = $(`
					<tr class="border-t">
						<td class="py-2 px-4 align-top">
							<div class="font-semibold text-blue-700">${server.id}</div>
							<div class="text-xs text-gray-600">${server.region}</div>
							<div class="text-xs text-gray-400">${server.port} • ${server.user_name}</div>
						</td>
						<td class="py-2 px-4 align-middle">
							${flagImg}${server.region}
						</td>
						<td class="py-2 px-4 align-middle">${server.ip_address || '-'}</td>
						<td class="py-2 px-4 align-middle">
							<span class="inline-flex items-center text-green-600 font-medium">
								▶ ${server.status || 'Unknown'}
							</span>
						</td>
						<td class="py-2 px-4 align-middle text-gray-400">...</td>
					</tr>
				`);
				tbody.append(row);
			});
		}
	});

	// + Add button → go to instances page
	container.find("#add-server").on("click", function() {
		frappe.set_route("instances");
	});
};
