---
parent: Scratch book
nav_order: 5
layout: default
---

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
        const newHTML = `<thead> <tr> <th>Topic</th> <th>Subtopic</th> <th>Subub topic</th> <th>Status</th> </tr> </thead> <tbody> <tr> <td>Architecture and design</td> <td>System Design</td> <td>Distributed Systems</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>System Design</td> <td>Scalablity</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>System Design</td> <td>Resilience</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Microservices</td> <td>Microservice Architecture</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Microservices</td> <td>API Gateways like vinz tyk zuul</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Communication</td> <td>REST</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Communication</td> <td>SOAP</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Communication</td> <td>gRPC</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Communication</td> <td>eventDrive/Kafka</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Communication</td> <td>MQ</td> <td>&nbsp;</td> </tr> <tr> <td>Architecture and design</td> <td>Design</td> <td>Design Patterns like singleton</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Java Basics</td> <td>Syntax</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Java Basics</td> <td>JVM Working</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Java Basics</td> <td>Interpreter vs Compiler</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Java Basics</td> <td>Collections</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Java Basics</td> <td>New additions Records, Sealed classes</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Concurrency and Threading</td> <td>Concurrency</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Concurrency and Threading</td> <td>Deadlock</td> <td>&nbsp;</td> </tr> <tr> <td>Java</td> <td>Concurrency and Threading</td> <td>Race Conditions</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Springboot</td> <td>&nbsp;</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Testing</td> <td>BDD</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Testing</td> <td>TDD</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Testing</td> <td>JUnit, Mockito and TestContainers</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Persistence and ORM</td> <td>Hibernate/JPA</td> <td>&nbsp;</td> </tr> <tr> <td>Frameworks and Ecosystem</td> <td>Persistence and ORM</td> <td>DB Transaction management</td> <td>&nbsp;</td> </tr> <tr> <td>Certifications</td> <td>AWS CP</td> <td>&nbsp;</td> <td>&nbsp;</td> </tr> <tr> <td>Certifications</td> <td>AWS SA</td> <td>&nbsp;</td> <td>&nbsp;</td> </tr> </tbody>`;

        table.innerHTML = newHTML;
        console.log("Table content updated successfully!");
    });
</script>