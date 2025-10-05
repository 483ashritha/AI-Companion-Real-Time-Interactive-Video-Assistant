describe('Home -> Companions -> Call flow (smoke)', () => {
  it('visits home and navigates to companions', () => {
    cy.visit('/');
    cy.contains('AI Companion');
    cy.contains('Browse Companions').click();
    cy.url().should('include', '/companions');
  });
});
