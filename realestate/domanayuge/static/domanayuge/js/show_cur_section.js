/**
 * Show current section in main menu
 */

var sectionID = document.querySelector('.section-content').id;
var linksMenu = document.querySelectorAll('#mainNav .page-scroll');

for (var i = 0; i < linksMenu.length; i++) {
    var attrHref = linksMenu[i].getAttribute('href');
    if (attrHref === '/' + sectionID) {
        linksMenu[i].closest('li').classList.add('active');
    }
}