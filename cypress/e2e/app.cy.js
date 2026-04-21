describe('E2E Benchmark Demo App', () => {
  it('login add-to-cart checkout flow', () => {
    cy.visit('/');

    cy.get('[data-testid="app-title"]').should('contain', 'E2E Benchmark Demo App');

    cy.get('[data-testid="username-input"]').type('testuser');
    cy.get('[data-testid="password-input"]').type('123456');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="product-card-1"]').should('be.visible');

    cy.get('[data-testid="add-to-cart-1"]').click();
    cy.get('[data-testid="cart-count"]').should('have.text', '1');
    cy.get('[data-testid="cart-success"]').should('contain', 'sepete eklendi');

    cy.get('[data-testid="fullname-input"]').type('Huseyin Emecen');
    cy.get('[data-testid="address-input"]').type('Ankara, Turkiye');
    cy.get('[data-testid="checkout-button"]').click();

    cy.get('[data-testid="order-success"]').should('contain', 'Sipariş başarıyla tamamlandı');
  });

  it('invalid login shows error', () => {
    cy.visit('/');

    cy.get('[data-testid="username-input"]').type('wronguser');
    cy.get('[data-testid="password-input"]').type('wrongpass');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="login-error"]').should('contain', 'Geçersiz kullanıcı adı veya parola');
  });

  it('checkout without cart shows error', () => {
    cy.visit('/');

    cy.get('[data-testid="username-input"]').type('testuser');
    cy.get('[data-testid="password-input"]').type('123456');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="fullname-input"]').type('Huseyin Emecen');
    cy.get('[data-testid="address-input"]').type('Ankara, Turkiye');
    cy.get('[data-testid="checkout-button"]').click();

    cy.get('[data-testid="checkout-error"]').should('contain', 'önce sepete ürün ekleyiniz');
  });
});
