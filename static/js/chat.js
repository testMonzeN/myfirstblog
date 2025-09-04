document.addEventListener('DOMContentLoaded', function() {
    const roomNameElement = document.getElementById('room-name');
    const userNameElement = document.getElementById('user-name');
    
    if (!roomNameElement || !userNameElement) {
        return; // Если мы не на странице чата, выходим
    }
    
    const roomName = roomNameElement.dataset.roomName;
    const userName = userNameElement.dataset.userName;
    
    const messagesContainer = document.querySelector('#chat-messages');
    const messageInput = document.querySelector('#chat-message-input');
    const messageSubmit = document.querySelector('#chat-message-submit');
    
    // Элементы для загрузки изображений
    const imageUploadBtn = document.getElementById('image-upload-btn');
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const cancelImageBtn = document.getElementById('cancel-image');
    const sendImageBtn = document.getElementById('send-image');
    
    // Проверяем поддержку WebSocket
    if (!window.WebSocket) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Ваш браузер не поддерживает WebSocket. Чат не будет работать.';
        messagesContainer.appendChild(errorDiv);
        return;
    }
    
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    // Прокрутка вниз к последнему сообщению
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Изначально прокручиваем вниз
    scrollToBottom();
    
    // Массив для отслеживания отображенных изображений (избежание дубликатов)
    const displayedImageIds = new Set();
    
    // Инициализируем список уже отображенных сообщений с изображениями из БД
    const existingMessages = messagesContainer.querySelectorAll('.message[data-message-id]');
    existingMessages.forEach(messageElement => {
        const messageId = messageElement.getAttribute('data-message-id');
        if (messageId && messageElement.querySelector('.message-image')) {
            displayedImageIds.add(messageId);
            console.log('Existing image message ID added to tracking:', messageId);
        }
    });
    
    // Получение сообщения от WebSocket
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        
        // Проверяем на дубликаты сообщений (как текстовых, так и с изображениями)
        if (data.message_id) {
            if (displayedImageIds.has(data.message_id)) {
                console.log('Duplicate message ignored (ID: ' + data.message_id + ', type: ' + (data.message_type || 'text') + ')');
                return;
            }
            // Добавляем ID только для сообщений с изображениями
            if (data.message_type === 'image') {
                displayedImageIds.add(data.message_id);
            }
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message' + (data.author === userName ? ' message-own' : '');
        
        // Добавляем data-message-id для отслеживания
        if (data.message_id) {
            messageElement.setAttribute('data-message-id', data.message_id);
        }
        
        const currentTime = new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        let messageContent = '';
        if (data.message_type === 'image') {
            messageContent = `<img src="${data.image_url}" alt="Изображение" class="message-image" onclick="openImageModal('${data.image_url}')" data-message-id="${data.message_id || ''}">`;
        } else {
            messageContent = data.message || '';
        }
        
        messageElement.innerHTML = `
            <div class="message-header">
                <strong class="message-author">${data.author}</strong>
                <small class="message-time">${currentTime}</small>
            </div>
            <div class="message-content">
                ${messageContent}
            </div>
        `;
        
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-warning';
        errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Соединение с чатом потеряно. Попробуйте обновить страницу.';
        messagesContainer.appendChild(errorDiv);
        scrollToBottom();
    };

    chatSocket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'type': 'text'
            }));
            messageInput.value = '';
        }
    }

    if (messageSubmit) {
        messageSubmit.addEventListener('click', sendMessage);
    }

    if (messageInput) {
        messageInput.addEventListener('keyup', function(e) {
            if (e.keyCode === 13) {  // Enter key
                sendMessage();
            }
        });

        messageInput.focus();
    }
   
    if (imageUploadBtn && imageInput) {
        console.log('Image upload elements found, setting up handlers...');
        
        imageUploadBtn.addEventListener('click', function() {
            console.log('Image upload button clicked');
            imageInput.click();
        });

        imageInput.addEventListener('change', function(e) {
            console.log('File selected:', e.target.files[0]);
            const file = e.target.files[0];
            if (file) {
                // Лимит
                if (file.size > 5 * 1024 * 1024) {
                    alert('Файл слишком большой. Максимальный размер: 5MB');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (previewImg) {
                        previewImg.src = e.target.result;
                        if (imagePreview) {
                            imagePreview.style.display = 'block';
                        }
                    }
                };
                reader.readAsDataURL(file);
            }
        });

        if (cancelImageBtn) {
            cancelImageBtn.addEventListener('click', function() {
                console.log('Cancel image clicked');
                imageInput.value = '';
                if (imagePreview) {
                    imagePreview.style.display = 'none';
                }
            });
        }

        if (sendImageBtn) {
            sendImageBtn.addEventListener('click', function() {
                console.log('Send image clicked');
                const file = imageInput.files[0];
                if (file) {
                    uploadImage(file);
                } else {
                    console.log('No file selected');
                }
            });
        }
    } else {
        console.log('Image upload elements not found!');
    }

    function uploadImage(file) {
        console.log('Starting image upload:', file.name, file.size, file.type);
        console.log('Room name:', roomName);
        
        const formData = new FormData();
        formData.append('image', file);
        formData.append('group_id', roomName);

        if (sendImageBtn) {
            sendImageBtn.disabled = true;
            sendImageBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Загружается...';
        }

        fetch('/chat/upload-image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                console.log('Upload successful!');
                
                // Отправляем WebSocket уведомление для отображения в реальном времени
                // ID будет добавлен в onmessage обработчике
                chatSocket.send(JSON.stringify({
                    'type': 'image',
                    'image_url': data.image_url,
                    'message_id': data.message_id
                }));
                
                // Скрываем предпросмотр
                imageInput.value = '';
                if (imagePreview) {
                    imagePreview.style.display = 'none';
                }
                
                // Показываем успешное сообщение
                showSuccessMessage('Изображение успешно отправлено!');
                
                // Примечание: Изображение появится через WebSocket уведомление
                
            } else {
                console.error('Upload failed:', data.error);
                alert('Ошибка загрузки изображения: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('Произошла ошибка при загрузке изображения: ' + error.message);
        })
        .finally(() => {
            if (sendImageBtn) {
                sendImageBtn.disabled = false;
                sendImageBtn.innerHTML = 'Отправить фото';
            }
        });
    }

    // Функция для добавления изображения в чат
    function addImageMessage(imageUrl, author) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message' + (author === userName ? ' message-own' : '');
        
        const currentTime = new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        messageElement.innerHTML = `
            <div class="message-header">
                <strong class="message-author">${author}</strong>
                <small class="message-time">${currentTime}</small>
            </div>
            <div class="message-content">
                <img src="${imageUrl}" alt="Изображение" class="message-image" onclick="openImageModal('${imageUrl}')">
            </div>
        `;
        
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Функция для показа успешного сообщения
    function showSuccessMessage(message) {
        const successMsg = document.createElement('div');
        successMsg.className = 'alert alert-success';
        successMsg.innerHTML = '<i class="fas fa-check"></i> ' + message;
        successMsg.style.position = 'fixed';
        successMsg.style.top = '20px';
        successMsg.style.right = '20px';
        successMsg.style.zIndex = '9999';
        successMsg.style.maxWidth = '300px';
        document.body.appendChild(successMsg);
        
        setTimeout(() => {
            if (successMsg.parentNode) {
                successMsg.parentNode.removeChild(successMsg);
            }
        }, 5000);
    }

    // Функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Функция для открытия изображения в модальном окне
    window.openImageModal = function(imageSrc) {
        const modalImage = document.getElementById('modal-image');
        if (modalImage) {
            modalImage.src = imageSrc;
            const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
            imageModal.show();
        }
    }
});
