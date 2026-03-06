---
parent: Programming Core
nav_order: 2
layout: default
---

# Concepts

1. POM vs BOM
   - Project Object Model vs Bill of Materials
   - | Aspect                      | POM                         | BOM                        |
     | --------------------------- | --------------------------- | -------------------------- |
     | Purpose                     | Build & configure a project | Manage dependency versions |
     | Has code                    | Yes                         | Usually no                 |
     | Produces artifact           | Yes (jar/war)               | No (pom only)              |
     | Uses `dependencyManagement` | Optional                    | Required                   |
     | One per project             | Yes                         | Shared across projects     |
