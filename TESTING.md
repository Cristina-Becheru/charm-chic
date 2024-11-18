## Table of Contents

1. [Automated Testing](#automated-testing)
   - [HTML Validation](#html-validation)
   - [CSS Validation](#css-validation)
   - [Python Testing](#python-testing)
2. [Manual Testing](#manual-testing)
   - [Responsivity Testing](#responsivity-testing)
   - [Page Testing](#page-testing)
     - [Navigation Bar Testing](#navigation-bar-testing)
     - [Toast Notifications Testing](#toast-notifications-testing)
     - [Key Feature Testing](#key-feature-testing)
3. [Lighthouse Testing](#lighthouse-testing)

---

## Automated Testing

### HTML Validation
Validated using [W3C HTML Validator](https://validator.w3.org/):
| Page                 | Errors? | Resolved Issues                          |
|----------------------|:-------:|------------------------------------------|
| Home Page            |    ✓    | Fixed missing `alt` attributes for images. |
| All Products Page    |    ✓    | Corrected duplicate IDs for sorting dropdown. |
| Product Detail Page  |    ✓    | Fixed unclosed `<div>` tag.              |
| Shopping Bag Page    |    ✓    | Replaced deprecated `<center>` tag with CSS alignment. |
| Checkout Page        |    ✓    | Corrected a missing `label` for input fields. |
| About Us Page        |    ✓    | Fixed invalid nesting of `<p>` within `<ul>`. |

---

### CSS Validation
Validated using [W3C CSS Validator](https://jigsaw.w3.org/css-validator/):
| File                | Errors? | Resolved Issues                          |
|---------------------|:-------:|------------------------------------------|
| `base.css`          |    ✓    | Removed invalid property `background-color: 10px;`. |
| `checkout.css`      |    ✓    | Fixed improper use of `z-index` without `position`. |
| `profile.css`       |    ✓    | Replaced invalid `float: center;` with `margin: auto;`. |
| `products.css`      |    ✓    | Corrected a missing semicolon in a media query. |

---

### Python Testing
All Python files were validated using [PEP8 Linter](https://pep8.org/) to ensure code quality and adherence to Python style guidelines.

| File                     | Errors? | Resolved Issues                          |
|--------------------------|:-------:|------------------------------------------|
| `models.py`              |    ✓    | Fixed missing docstring for class definitions. |
| `views.py`               |    ✓    | Corrected inconsistent indentation in one function. |
| `forms.py`               |    ✓    | Removed unused imports that caused linting warnings. |
| `urls.py`                |    ✓    | Corrected trailing comma in urlpatterns list. |
| `signals.py`             |    ✓    | Fixed a typo in signal handler function name. |
| `webhooks.py`            |    ✓    | Removed unnecessary print statements used for debugging. |

---

### Manual Testing Notes
While Lighthouse testing was conducted on most pages, the **Home Page** underwent **manual testing** due to its dynamic elements (e.g., video backgrounds and JavaScript-powered components). This approach ensured that all interactive and design features, such as the hero section and navigation bar, functioned correctly across different devices and browsers.

---

## Manual Testing

### Responsivity Testing

The site was rigorously tested across multiple device sizes to ensure a seamless and user-friendly experience. The following table outlines the results of the responsiveness tests:

| **Responsivity**            | **Mobile S (320px)** | **Mobile L (425px)** | **Tablet (768px)** | **Desktop (1024px)** |
|-----------------------------|:-------------------:|:--------------------:|:------------------:|:-------------------:|
| Responsive UI Components    |         ✓          |         ✓           |         ✓         |         ✓          |
| Text Adjusts Dynamically    |         ✓          |         ✓           |         ✓         |         ✓          |
| Forms are Fully Functional  |         ✓          |         ✓           |         ✓         |         ✓          |
| Button Placement is Intuitive |       ✓          |         ✓           |         ✓         |         ✓          |
| Navigation Bar is Adaptable |         ✓          |         ✓           |         ✓         |         ✓          |
| Footer Scales Effectively   |         ✓          |         ✓           |         ✓         |         ✓          |

The design responds effectively across all tested screen resolutions, maintaining visual consistency and functionality.

---

### Page Testing

#### Navigation Bar Testing
The navigation bar was tested for usability and responsiveness across all views. The following scenarios were validated:

| **Test**                                              | **Result** |
|-------------------------------------------------------|:----------:|
| Navigation links and styles load correctly            |     ✓      |
| Navigation adjusts dynamically on mobile              |     ✓      |
| All links function as expected                        |     ✓      |
| Brand logo redirects users to the home page           |     ✓      |
| Admin-specific links appear when logged in as admin   |     ✓      |
| User-specific links appear when logged in as a shopper|     ✓      |
| Anonymous users see login and register options only   |     ✓      |
| Dropdowns work smoothly in smaller screens            |     ✓      |
| Shopping bag total updates dynamically in real-time   |     ✓      |

---

#### Toast Notifications Testing
Toasts were tested to ensure users receive clear feedback on actions taken throughout the platform:

| **Test**                                       | **Result** |
|-----------------------------------------------|:----------:|
| Error toasts display during invalid operations|     ✓      |
| Success toasts confirm user actions (e.g., added to cart) | ✓ |
| Toasts dynamically update with relevant information | ✓ |
| Toasts do not obstruct the main UI or functionality | ✓ |

---

#### Key Feature Testing

1. **Home Page:**
   - Hero section displays correctly with interactive elements.
   - Call-to-action buttons redirect users appropriately.
   - Mobile users experience smooth scrolling and responsive visuals.

2. **Products Page:**
   - Products load dynamically with accurate data.
   - Sorting and filtering options function correctly.
   - Pagination adjusts based on the number of available products.

3. **Product Detail Page:**
   - Accurate product details are shown, including category and tags.
   - Size and quantity selection inputs work as expected.
   - Related products are displayed based on the category.

4. **Shopping Bag:**
   - Bag updates in real-time when items are added or removed.
   - Subtotal and delivery charges are calculated correctly.
   - Error handling is in place for invalid inputs.

5. **Checkout:**
   - Secure form validations are implemented for all fields.
   - Stripe integration ensures secure payment processing.
   - Users are redirected to a confirmation page upon order success.

6. **Profile:**
   - Users can update delivery preferences and view order history.
   - Data persists accurately between sessions.

7. **Admin Features:**
   - Admin users can add, edit, and delete products without errors.
   - Changes reflect instantly on the products page.

---

## Lighthouse Testing

Lighthouse was used to test the performance, accessibility, best practices, and SEO of the website. The following pages were evaluated to ensure optimal user experience:

1. **Home Page Lighthouse Results**:
   ![Home Page Lighthouse Results](static/images/homelighthouse.png)

2. **Contact Page Lighthouse Results**:
   ![Contact Page Lighthouse Results](static/images/contact.png)

3. **Checkout Page Lighthouse Results**:
   ![Checkout Page Lighthouse Results](static/images/checkout.png)

4. **Product Detail Page Lighthouse Results**:
   ![Product Detail Page Lighthouse Results](static/images/productdetail.png)

5. **Products Page Lighthouse Results**:
   ![Products Page Lighthouse Results](static/images/products.png)

6. **Profile Page Lighthouse Results**:
   ![Profile Page Lighthouse Results](static/images/profile.png)

7. **Shopping Bag Page Lighthouse Results**:
   ![Shopping Bag Page Lighthouse Results](static/images/shoppingbag.png)

8. **Sign In Page Lighthouse Results**:
   ![Sign In Page Lighthouse Results](static/images/signin.png)

9. **Sign Up Page Lighthouse Results**:
   ![Sign Up Page Lighthouse Results](static/images/signup.png)

