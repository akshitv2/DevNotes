# Dynamic Table Example

This table is styled by Jekyll, but the content will be replaced by JavaScript on page load.

<div id="table-container">
    <table id="target-table">
        <thead>
            <tr>
                <th>Placeholder Header</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Loading data...</td>
            </tr>
        </tbody>
    </table>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const table = document.getElementById('target-table');
        const newHTML = `
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Gemini AI Tool</td>
                    <td>$0 (Free Tier)</td>
                    <td>Active</td>
                </tr>
                <tr>
                    <td>GitHub Pages</td>
                    <td>$0 (Free)</td>
                    <td>Active</td>
                </tr>
            </tbody>`;

        table.innerHTML = newHTML;
        console.log("Table content updated successfully!");
    });
</script>