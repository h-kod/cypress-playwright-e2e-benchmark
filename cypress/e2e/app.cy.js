const activeProfile = Cypress.env('PROFILE_MODE') || 'all';

function includeProfile(profile) {
  return activeProfile === 'all' || activeProfile === profile;
}

function loginAndOpenProfiles() {
  cy.visit('/');
  cy.get('[data-testid="username-input"]').type('testuser');
  cy.get('[data-testid="password-input"]').type('123456');
  cy.get('[data-testid="login-button"]').click();
}

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

  if (includeProfile('ui-heavy')) {
    it('ui-heavy profile starts, filters, and completes with visible UI output', () => {
      loginAndOpenProfiles();
      cy.get('[data-testid="profile-tab-ui"]').click();
      cy.get('[data-testid="profile-tab-ui"]').should('have.class', 'active');
      cy.get('[data-testid="ui-heavy-profile"]').should('be.visible');
      cy.get('[data-testid="ui-heavy-summary"]').should('contain', 'Gösterilen öğe sayısı: 36');
      cy.get('[data-testid="ui-heavy-item"]').should('have.length', 36);
      cy.get('[data-testid="ui-filter-input"]').type('cart drawer 2');
      cy.get('[data-testid="ui-heavy-summary"]').should('contain', '1');
      cy.get('[data-testid="ui-heavy-item"]').should('have.length', 1);
      cy.get('[data-testid="ui-sort-button"]').click();
      cy.get('[data-testid="ui-heavy-list"]').should('contain', 'Cart Drawer 2');
    });
  }

  if (includeProfile('cpu-heavy')) {
    it('cpu-heavy profile starts, runs computation, and shows deterministic result', () => {
      loginAndOpenProfiles();
      cy.get('[data-testid="profile-tab-cpu"]').click();
      cy.get('[data-testid="profile-tab-cpu"]').should('have.class', 'active');
      cy.get('[data-testid="cpu-heavy-profile"]').should('be.visible');
      cy.get('[data-testid="cpu-heavy-status"]').should('contain', 'Son sonuç hazır değil.');
      cy.get('[data-testid="cpu-run-button"]').click();
      cy.get('[data-testid="cpu-heavy-status"]').should('have.attr', 'data-cpu-result');
      cy.get('[data-testid="cpu-heavy-status"]').should('contain', 'Son sonuç: ');
      cy.get('[data-testid="cpu-heavy-status"]')
        .invoke('attr', 'data-cpu-result')
        .should('match', /^\d+$/);
    });
  }

  if (includeProfile('ram-heavy')) {
    it('ram-heavy profile starts, allocates memory, and releases it', () => {
      loginAndOpenProfiles();
      cy.get('[data-testid="profile-tab-ram"]').click();
      cy.get('[data-testid="profile-tab-ram"]').should('have.class', 'active');
      cy.get('[data-testid="ram-heavy-profile"]').should('be.visible');
      cy.get('[data-testid="ram-heavy-status"]').should('contain', 'Bellek yükü oluşturulmadı.');
      cy.get('[data-testid="ram-allocate-button"]').click();
      cy.get('[data-testid="ram-heavy-status"]').should('have.attr', 'data-ram-block-count', '48');
      cy.get('[data-testid="ram-heavy-status"]').should('contain', 'Blok sayısı: 48');
      cy.get('[data-testid="ram-release-button"]').click();
      cy.get('[data-testid="ram-heavy-status"]').should('have.attr', 'data-ram-block-count', '0');
      cy.get('[data-testid="ram-heavy-status"]').should('contain', 'Bellek yükü serbest bırakıldı.');
    });
  }
});
