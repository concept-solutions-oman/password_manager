/** @odoo-module */

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SimpleCopyClipboard extends Component {
    setup() {
        this.notification = useService("notification");
    }

    get formattedValue() {
        // Check if password="True" attribute was passed (often passed in options or attrs, but standardProps has context/etc)
        // A simple way is dealing with the node options or field info.
        // For Odoo 17, let's treat it simple: if props.userInfo.password is true... wait props are complex.

        // Let's rely on props.value (which is the raw value).
        // If we want to mask it, we need to know if it's a password field.
        // The view xml will have widget="simple_copy" password="True" ??
        // Attributes like password="True" are not automatically passed as props to the component unless defined in extractProps.

        // However, for this specific use case, we can pass an option `{'password': true}` in the widget options, 
        // OR simpler: we check if the field name contains 'password'.
        if (this.props.record.fields[this.props.name].type === 'char' && (this.props.name.includes('password'))) {
            return "••••••••";
        }
        return this.props.record.data[this.props.name];
    }

    async onCopy() {
        const value = this.props.record.data[this.props.name];
        if (!value) return;

        try {
            await navigator.clipboard.writeText(value);
            this.notification.add("Copied to clipboard", { type: "success" });
        } catch (error) {
            this.notification.add("Failed to copy", { type: "danger" });
        }
    }
}

SimpleCopyClipboard.template = "concept_password.SimpleCopyClipboard";
SimpleCopyClipboard.props = {
    ...standardFieldProps,
};

export const simpleCopyClipboard = {
    component: SimpleCopyClipboard,
    displayName: "Simple Copy",
    supportedTypes: ["char"],
};

registry.category("fields").add("simple_copy", simpleCopyClipboard);
