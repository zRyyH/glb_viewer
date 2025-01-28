text1 = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador de Modelo IFC</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #1e1e2f;
            font-family: 'Roboto', Arial, sans-serif;
        }
        canvas {
            display: block;
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Roboto', Arial, sans-serif;
            font-size: 1.5rem;
            color: #333;
            text-align: center;
        }
        #spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(50, 50, 50, 0.1);
            border-top: 5px solid #333;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #controls {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 10;
            background-color: rgba(30, 30, 47, 0.33);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Roboto', Arial, sans-serif;
            color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        #controls label {
            font-weight: bold;
            display: block;
            margin-bottom: 8px;
        }
        #controls select,
        #controls button {
            width: 100%;
            padding: 8px;
            border-radius: 4px;
            border: none;
            outline: none;
            margin-bottom: 8px;
            font-family: 'Roboto', Arial, sans-serif;
        }
        #controls button {
            background-color: #444;
            color: #fff;
            cursor: pointer;
        }
        #controls button:hover {
            background-color: #555;
        }
        #info-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            color: #fff;
            font-family: 'Roboto', Arial, sans-serif;
            font-size: 14px;
            padding: 10px;
            box-sizing: border-box;
            z-index: 10;
            display: flex;
            justify-content: flex-start;
            align-items: center;
        }
        #info-bar span {
            margin: 0 10px;
        }
    </style>
</head>
<body>
    <div id="loading">
        <div id="spinner"></div>
        <span>Carregando, por favor aguarde...</span>
    </div>
    <div id="controls">
        <label for="view-mode">Modo de visualização:</label>
        <select id="view-mode">
            <option value="normal">Normal</option>
            <option value="wireframe">Wireframe</option>
        </select>
        <label for="background-color">Cor de Fundo:</label>
        <select id="background-color">
            <option value="#e0e0e0" selected>Cinza</option>
            <option value="#1e1e2f">Escuro</option>
            <option value="#ffffff">Claro</option>
        </select>
        <button id="toggle-autorotate">Ativar Rotação Automática</button>
    </div>
    <div id="info-bar">
        <span id="dimensions">Dimensões: -</span>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Configuração da cena
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xe0e0e0); // Fundo padrão Cinza

        // Configuração da câmera
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 10);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Controles de órbita
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.1;
        controls.autoRotate = false; // Rotação automática desativada por padrão
        controls.autoRotateSpeed = 2; // Velocidade da rotação automática

        // Iluminação aprimorada
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.5);
        hemiLight.position.set(0, 50, 0);
        scene.add(hemiLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(0, 20, 10);
        scene.add(dirLight);

        // Atualizar informações do projeto
        function updateInfoBar(dimensions) {
            document.getElementById('dimensions').innerText = `Dimensões: ${dimensions.x.toFixed(2)} x ${dimensions.y.toFixed(2)} x ${dimensions.z.toFixed(2)}`;
        }

        // Carregamento do modelo GLB
        const loader = new THREE.GLTFLoader();
        let model;
        let originalMaterials = new Map(); // Armazena os materiais originais
"""
text2 = """
            // Centralizar o modelo
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            model.position.sub(center);
            model.position.y -= size.y / 2;

            model.scale.set(1, 1, 1);
            scene.add(model);

            document.getElementById('loading').style.display = 'none';

            controls.target.set(0, 0, 0);
            controls.update();

            const maxDim = Math.max(size.x, size.y, size.z);
            camera.position.set(maxDim * 1.5, maxDim * 1.5, maxDim * 1.5);
            camera.lookAt(0, 0, 0);

            // Atualiza a barra de informações
            updateInfoBar(size);

            // Armazena os materiais originais
            model.traverse((child) => {
                if (child.isMesh) {
                    originalMaterials.set(child, child.material);
                }
            });

            // Alternar entre modos de visualização
            const viewModeSelect = document.getElementById('view-mode');
            viewModeSelect.addEventListener('change', () => {
                const mode = viewModeSelect.value;
                model.traverse((child) => {
                    if (child.isMesh) {
                        if (mode === 'wireframe') {
                            child.material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
                        } else if (mode === 'normal') {
                            child.material = originalMaterials.get(child);
                        }
                    }
                });
            });

            // Alterar cor de fundo
            const bgColorSelect = document.getElementById('background-color');
            bgColorSelect.addEventListener('change', () => {
                const color = bgColorSelect.value;
                scene.background = new THREE.Color(color);
            });

            // Alternar rotação automática
            const toggleAutorotateButton = document.getElementById('toggle-autorotate');
            toggleAutorotateButton.addEventListener('click', () => {
                controls.autoRotate = !controls.autoRotate;
                toggleAutorotateButton.innerText = controls.autoRotate
                    ? 'Desativar Rotação Automática'
                    : 'Ativar Rotação Automática';
            });
        }, undefined, (error) => {
            console.error('Erro ao carregar o modelo IFC:', error);
            document.getElementById('loading').innerText = 'Erro ao carregar o modelo!';
        });

        function animate() {
            controls.update();
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

def get_html(api_endpoint, url_encode):
    center = "loader.load" + "('{}/{}'".format(api_endpoint, url_encode) + ", (gltf) => { model = gltf.scene;"
    return text1 + center + text2