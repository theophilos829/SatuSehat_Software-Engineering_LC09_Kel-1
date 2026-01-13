// Tab switching
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('text-blue-600', 'border-blue-600'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.add('text-gray-500'));
        button.classList.remove('text-gray-500');
        button.classList.add('text-blue-600', 'border-blue-600');

        // Show content
        const tab = button.dataset.tab;
        document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
        document.getElementById(tab).classList.remove('hidden');
    });
});

// Load data on start
async function loadData() {
    const res = await fetch('/api/data');
    const data = await res.json();
    
    // Update profile display
    const profileDiv = document.getElementById('profile-display');
    if (data.profile && Object.keys(data.profile).length > 0) {
        profileDiv.innerHTML = `
            <p><strong>Nama:</strong> ${data.profile.nama}</p>
            <p><strong>Usia:</strong> ${data.profile.usia} tahun</p>
            <p><strong>Jenis Kelamin:</strong> ${data.profile.jenis_kelamin === 'L' ? 'Laki-laki' : 'Perempuan'}</p>
        `;
    }

    // Update history
    const historyList = document.getElementById('history-list');
    if (data.history && data.history.length > 0) {
        historyList.innerHTML = data.history.reverse().map(item => `
            <div class="p-3 bg-gray-50 rounded-lg">
                <div class="text-sm text-gray-500">${item.timestamp}</div>
                <div><strong>Gejala:</strong> ${item.gejala}</div>
                <div><strong>Rekomendasi:</strong> ${item.rekomendasi}</div>
            </div>
        `).join('');
    }
}

// Edit profile modal
document.getElementById('edit-profile-btn').addEventListener('click', async () => {
    const res = await fetch('/api/data');
    const data = await res.json();
    const p = data.profile || {};
    document.getElementById('modal-nama').value = p.nama || '';
    document.getElementById('modal-usia').value = p.usia || '';
    document.getElementById('modal-jk').value = p.jenis_kelamin || '';
    document.getElementById('profile-modal').classList.remove('hidden');
});

document.getElementById('cancel-profile').addEventListener('click', () => {
    document.getElementById('profile-modal').classList.add('hidden');
});

document.getElementById('save-profile').addEventListener('click', async () => {
    const profile = {
        nama: document.getElementById('modal-nama').value,
        usia: parseInt(document.getElementById('modal-usia').value),
        jenis_kelamin: document.getElementById('modal-jk').value
    };
    if (!profile.nama || !profile.usia || !profile.jenis_kelamin) {
        alert('Harap isi semua kolom!');
        return;
    }
    await fetch('/api/profile', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(profile)
    });
    document.getElementById('profile-modal').classList.add('hidden');
    loadData();
});

// Cek gejala
document.getElementById('check-btn').addEventListener('click', async () => {
    let symptom = document.getElementById('symptom-select').value;
    if (!symptom) symptom = document.getElementById('manual-symptom').value.trim();
    if (!symptom) {
        alert('Silakan masukkan gejala terlebih dahulu.');
        return;
    }

    const res = await fetch('/api/check', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({symptom})
    });
    const result = await res.json();

    document.getElementById('recommendation').innerText = result.rekomendasi;
    document.getElementById('result').classList.remove('hidden');
    loadData(); // Refresh riwayat
});

// Init
loadData();