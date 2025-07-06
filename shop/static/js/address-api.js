/**
 * Address API Handler for Vietnam Provinces
 * Sử dụng API: https://provinces.open-api.vn/
 */

// Helper fetch qua proxy
function fetchProvincesProxy(apiPath) {
    return fetch(`/proxy-provinces/?url=https://provinces.open-api.vn/api/${apiPath}`)
        .then(res => res.json());
}

class AddressAPI {
    constructor() {
        this.baseURL = 'https://provinces.open-api.vn/api';
        this.provinceSelect = null;
        this.districtSelect = null;
        this.wardSelect = null;
        this.addressInput = null;
        this.isInitialized = false;
    }

    /**
     * Khởi tạo API địa chỉ
     * @param {string} provinceId - ID của select tỉnh/thành
     * @param {string} districtId - ID của select quận/huyện  
     * @param {string} wardId - ID của select phường/xã
     * @param {string} addressId - ID của input địa chỉ chi tiết
     */
    init(provinceId = 'province', districtId = 'district', wardId = 'ward', addressId = 'address') {
        this.provinceSelect = document.getElementById(provinceId);
        this.districtSelect = document.getElementById(districtId);
        this.wardSelect = document.getElementById(wardId);
        this.addressInput = document.getElementById(addressId);
        
        // Thêm các input hidden cho tên địa chỉ
        this.provinceNameInput = document.getElementById('province_name');
        this.districtNameInput = document.getElementById('district_name');
        this.wardNameInput = document.getElementById('ward_name');

        if (!this.provinceSelect || !this.districtSelect || !this.wardSelect) {
            console.error('AddressAPI: Không tìm thấy các element select cần thiết');
            return false;
        }

        this.setupEventListeners();
        this.loadProvinces();
        this.isInitialized = true;
        return true;
    }

    /**
     * Thiết lập event listeners
     */
    setupEventListeners() {
        // Khi chọn tỉnh/thành
        this.provinceSelect.addEventListener('change', () => {
            this.onProvinceChange();
        });

        // Khi chọn quận/huyện
        this.districtSelect.addEventListener('change', () => {
            this.onDistrictChange();
        });

        // Khi chọn phường/xã
        this.wardSelect.addEventListener('change', () => {
            this.onWardChange();
        });
    }

    /**
     * Hiển thị loading state
     */
    setLoading(select, isLoading, message = 'Đang tải...') {
        if (isLoading) {
            select.innerHTML = `<option value="">${message}</option>`;
            select.disabled = true;
        }
    }

    /**
     * Xử lý lỗi
     */
    handleError(select, message) {
        select.innerHTML = `<option value="">${message}</option>`;
        select.disabled = true;
        console.error('AddressAPI Error:', message);
    }

    /**
     * Tải danh sách tỉnh/thành
     */
    async loadProvinces() {
        this.setLoading(this.provinceSelect, true, 'Đang tải tỉnh/thành...');
        
        try {
            const provinces = await fetchProvincesProxy('p/');
            this.provinceSelect.innerHTML = '<option value="">Chọn tỉnh/thành</option>' +
                provinces.map(p => `<option value="${p.code}">${p.name}</option>`).join('');
            this.provinceSelect.disabled = false;
            
        } catch (error) {
            this.handleError(this.provinceSelect, 'Không thể tải danh sách tỉnh/thành');
        }
    }

    /**
     * Xử lý khi chọn tỉnh/thành
     */
    async onProvinceChange() {
        const provinceCode = this.provinceSelect.value;
        
        // Reset district và ward
        this.districtSelect.innerHTML = '<option value="">Chọn quận/huyện</option>';
        this.districtSelect.disabled = true;
        this.wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';
        this.wardSelect.disabled = true;
        
        // Reset tên địa chỉ
        if (this.provinceNameInput) this.provinceNameInput.value = '';
        if (this.districtNameInput) this.districtNameInput.value = '';
        if (this.wardNameInput) this.wardNameInput.value = '';

        if (!provinceCode) return;

        this.setLoading(this.districtSelect, true, 'Đang tải quận/huyện...');
        
        try {
            const data = await fetchProvincesProxy(`p/${provinceCode}?depth=2`);
            this.districtSelect.innerHTML = '<option value="">Chọn quận/huyện</option>' +
                data.districts.map(d => `<option value="${d.code}" data-name="${d.name}">${d.name}</option>`).join('');
            this.districtSelect.disabled = false;
            
            // Lưu tên tỉnh/thành
            if (this.provinceNameInput) {
                this.provinceNameInput.value = data.name || '';
            }
            
        } catch (error) {
            this.handleError(this.districtSelect, 'Không thể tải danh sách quận/huyện');
        }
    }

    /**
     * Xử lý khi chọn quận/huyện
     */
    async onDistrictChange() {
        const districtCode = this.districtSelect.value;
        
        // Reset ward
        this.wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';
        this.wardSelect.disabled = true;
        
        // Reset tên ward
        if (this.wardNameInput) this.wardNameInput.value = '';

        if (!districtCode) return;

        this.setLoading(this.wardSelect, true, 'Đang tải phường/xã...');
        
        try {
            const data = await fetchProvincesProxy(`d/${districtCode}?depth=2`);
            this.wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>' +
                data.wards.map(w => `<option value="${w.code}" data-name="${w.name}">${w.name}</option>`).join('');
            this.wardSelect.disabled = false;
            
            // Lưu tên quận/huyện
            if (this.districtNameInput) {
                this.districtNameInput.value = data.name || '';
            }
            
        } catch (error) {
            this.handleError(this.wardSelect, 'Không thể tải danh sách phường/xã');
        }
    }

    /**
     * Xử lý khi chọn phường/xã
     */
    onWardChange() {
        const wardCode = this.wardSelect.value;
        if (wardCode && this.wardNameInput) {
            // Lấy tên phường/xã từ option được chọn
            const selectedOption = this.wardSelect.options[this.wardSelect.selectedIndex];
            if (selectedOption) {
                this.wardNameInput.value = selectedOption.getAttribute('data-name') || selectedOption.text;
            }
        }
    }

    /**
     * Lấy địa chỉ đầy đủ
     */
    getFullAddress() {
        if (!this.isInitialized) return '';

        const province = this.provinceSelect.options[this.provinceSelect.selectedIndex]?.text || '';
        const district = this.districtSelect.options[this.districtSelect.selectedIndex]?.text || '';
        const ward = this.wardSelect.options[this.wardSelect.selectedIndex]?.text || '';
        const address = this.addressInput?.value || '';

        return `${address}, ${ward}, ${district}, ${province}`.replace(/^,\s*/, '').replace(/,\s*,/g, ',');
    }

    /**
     * Kiểm tra form hợp lệ
     */
    validateForm() {
        if (!this.isInitialized) return false;

        const province = this.provinceSelect.value;
        const district = this.districtSelect.value;
        const ward = this.wardSelect.value;
        const address = this.addressInput?.value?.trim();

        if (!province || !district || !ward) {
            alert('Vui lòng chọn đầy đủ tỉnh/thành, quận/huyện và phường/xã!');
            return false;
        }

        if (!address) {
            alert('Vui lòng nhập địa chỉ chi tiết!');
            if (this.addressInput) {
                this.addressInput.focus();
            }
            return false;
        }

        return true;
    }

    /**
     * Reset form
     */
    reset() {
        if (!this.isInitialized) return;

        this.provinceSelect.selectedIndex = 0;
        this.districtSelect.innerHTML = '<option value="">Chọn quận/huyện</option>';
        this.districtSelect.disabled = true;
        this.wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';
        this.wardSelect.disabled = true;
        
        if (this.addressInput) {
            this.addressInput.value = '';
        }
    }
}

// Khởi tạo global instance
window.addressAPI = new AddressAPI();

// Auto-init khi DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Tự động khởi tạo nếu có các element cần thiết
    if (document.getElementById('province') && 
        document.getElementById('district') && 
        document.getElementById('ward')) {
        window.addressAPI.init();
    }
}); 