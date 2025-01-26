text1 = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador de Modelo GLB</title>
    <style>
        body { margin: 0; overflow: hidden; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Configuração da cena
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xe0e0e0); // Fundo cinza claro para melhor contraste

        // Configuração da câmera
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 10);  // Melhor posicionamento inicial da câmera

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Controles manuais de órbita
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;  // Habilita suavização nos movimentos
        controls.dampingFactor = 0.1;   // Intensidade da suavização
        controls.enableZoom = true;     // Permite zoom manual
        controls.autoRotate = false;    // Desativa rotação automática
        controls.maxDistance = 100;     // Distância máxima do zoom
        controls.minDistance = 1;       // Distância mínima do zoom

        // Iluminação
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
        directionalLight.position.set(10, 20, 10);
        scene.add(directionalLight);

        // Carregamento do modelo GLB
        const loader = new THREE.GLTFLoader();
        let model;
"""
text2 = """
            // Centralizar o modelo
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            model.position.sub(center);  // Centraliza o modelo na origem
            model.position.y -= size.y / 2;  // Ajusta a altura do modelo para ficar acima do plano

            model.scale.set(1, 1, 1);  // Ajuste de escala se necessário
            scene.add(model);

            // Ajusta a câmera para olhar para o centro do modelo
            controls.target.set(0, 0, 0);
            controls.update();

            // Ajusta a câmera para enquadrar o modelo corretamente
            const maxDim = Math.max(size.x, size.y, size.z);
            camera.position.set(maxDim * 1.5, maxDim * 1.5, maxDim * 1.5);
            camera.lookAt(0, 0, 0);
        }, undefined, (error) => {
            console.error('Erro ao carregar o modelo GLB:', error);
        });

        // Função de renderização
        function animate() {
            controls.update(); // Atualiza os controles manualmente
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        animate();

        // Ajuste responsivo
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