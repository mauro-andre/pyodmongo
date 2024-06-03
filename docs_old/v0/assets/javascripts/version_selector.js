document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');

    function addVersionSelector() {
        var headerNav = document.querySelector('.md-header__topic');
        if (!headerNav) {
            console.log('Header nav not found, retrying...');
            setTimeout(addVersionSelector, 100); // Tenta novamente após 100ms
            return;
        }

        var selector = document.createElement('select');
        selector.onchange = function () {
            window.location.href = this.value;
        };

        var versions = {
            'v1': '/',
            'v0': '/v0/'
        };

        for (var version in versions) {
            var option = document.createElement('option');
            option.value = versions[version];
            option.textContent = version;
            if ((version === 'v1' && window.location.pathname === '/') ||
                (version !== 'v1' && window.location.pathname.startsWith(versions[version]))) {
                option.selected = true;
            }
            selector.appendChild(option);
        }

        headerNav.appendChild(selector);
        console.log('Selector added to header nav');
    }

    addVersionSelector();
});