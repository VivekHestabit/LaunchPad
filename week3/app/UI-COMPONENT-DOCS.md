
---

## Component Details

### 1. Badge
**File:** `components/ui/Badge.js`  
**Purpose:**  
Used to display small status labels, tags, or indicators such as status, roles, or categories.

**Used in:**  
- Tables
- Dashboard widgets

---

### 2. Button
**File:** `components/ui/Button.js`  
**Purpose:**  
Reusable button component supporting different variants (primary, secondary, danger, etc.).

**Used in:**  
- Forms (Sign In / Sign Up)
- Dashboard actions
- Modal actions

---

### 3. Card
**File:** `components/ui/Card.js`  
**Purpose:**  
Wrapper component for grouping related content inside a bordered container.

**Used in:**  
- Dashboard
- Tables page
- Landing page sections

---

### 4. Input
**File:** `components/ui/Input.js`  
**Purpose:**  
Reusable input field component for forms with consistent styling.

**Used in:**  
- Sign In page
- Sign Up page
- Form-based interactions

---

### 5. Modal
**File:** `components/ui/Modal.jsx`  
**Purpose:**  
Popup modal component for confirmations, forms, or alerts.

**Used in:**  
- Dashboard
- Tables page
- Any user action requiring confirmation

---

### 6. Navbar
**File:** `components/ui/Navbar.js`  
**Purpose:**  
Top navigation bar component used across public and authenticated pages.

**Used in:**  
- Landing page
- Dashboard
- Tables page

---

### 7. Sidebar
**File:** `components/ui/Sidebar.js`  
**Purpose:**  
Side navigation component for authenticated sections of the application.

**Used in:**  
- Dashboard
- Tables page

---

### 8. SignNav
**File:** `components/ui/SignNav.js`  
**Purpose:**  
Navigation bar specifically designed for the Sign In page.

**Used in:**  
- Sign In page

---

### 9. SignupNav
**File:** `components/ui/SignupNav.js`  
**Purpose:**  
Navigation bar specifically designed for the Sign Up page.

**Used in:**  
- Sign Up page

---

### 10. AOSProvider
**File:** `components/ui/AOSProvider.js`  
**Purpose:**  
Wrapper provider component to enable and manage AOS (Animate On Scroll) animations across the application.

**Used in:**  
- Root layout
- Landing page animations

---

## Notes

- All UI components are designed to be reusable and consistent across the application.
- Styling is managed globally using `globals.css`.
- Components follow a modular structure to improve maintainability and scalability.

---

## Future Enhancements

- Add theme support (dark/light mode)
- Add Storybook documentation for UI components
- Improve accessibility (ARIA attributes)
