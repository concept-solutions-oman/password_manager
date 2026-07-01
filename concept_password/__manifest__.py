{
    'name' : 'Concept Password Management',
    'author' : 'Concept Solutions',
    'sequence' : '0',
    'website': 'https://www.csloman.com',
    'summary': 'A centralized, ultra-secure hub for managing customer credentials, reducing search time and securing access.',
    'price': 49.00,
    'currency': 'USD',
    'images': ['static/description/main_screenshot.png'],
    'keywords': 'password management, credentials, security, access control, password manager, b2b',
    'description': """
Concept Password Management
===========================
A centralized, ultra-secure hub for managing your customer credentials.
Protect sensitive data, control access rights, and dramatically reduce the time spent searching for logins.

Why You Need This Module:
-------------------------
*   **Eliminate Endless Searching**: Reduces 90% of search time. Passwords are linked directly to customers and devices.
*   **Stop Insecure Sharing**: Store them centrally so only authorized personnel can view them when needed.
*   **Accelerate Workflows**: 1-click copy widgets and direct URL links.

Comprehensive Features:
-----------------------
*   **Centralized Password Hub**: Manage all passwords in one place. Visually masked by default.
*   **Device & App Tracking**: Categorize credentials by system type (e.g., Server, FTP, CMS, AWS).
*   **One-Click Smart Copy**: Instantly copy usernames and passwords to clipboard.
*   **Advanced Sidebar Filtering**: Filter thousands of records down to specific customers or devices.

Access Control:
---------------
*   **Administrator**: Full unrestricted access.
*   **Assigned Users Only**: Restricted access to view/interact with passwords for explicitly assigned customers or devices.
    """,
    'installable': True,
    'application': True,
    'version': '17.0.1.0',
    'category': 'Administrator',
    'depends' : ['mail', 'product', 'project'],
    'data' :[
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/update_password.xml',
        'views/menu.xml',
        'views/password_form_view.xml',
        'views/device_list_view.xml',
        'views/project_task_views.xml',
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
             'concept_password/static/src/js/simple_copy_clipboard.js',
             'concept_password/static/src/xml/simple_copy_clipboard.xml',
        ],
    },

    'license': 'LGPL-3',
}