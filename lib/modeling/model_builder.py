
# ssds part
from lib.modeling.ssds import ssd
from lib.modeling.ssds import ssd_lite
from lib.modeling.ssds import rfb
from lib.modeling.ssds import rfb_lite
from lib.modeling.ssds import fssd
from lib.modeling.ssds import fssd_lite
from lib.modeling.ssds import yolo
from lib.modeling.ssds import ssd_dual
from lib.modeling.ssds import ssd_lite_dualpath

ssds_map = {
                'ssd': ssd.build_ssd,
                'ssd_lite': ssd_lite.build_ssd_lite,
                'rfb': rfb.build_rfb,
                'rfb_lite': rfb_lite.build_rfb_lite,
                'fssd': fssd.build_fssd,
                'fssd_lite': fssd_lite.build_fssd_lite,
                'yolo_v2': yolo.build_yolo_v2,
                'yolo_v3': yolo.build_yolo_v3,
                'ssd_dual': ssd_dual.build_ssd_dual,
                'ssd_lite_dual': ssd_lite_dualpath.build_ssd_lite_dual
            }

# nets part
from lib.modeling.nets import vgg
from lib.modeling.nets import resnet
from lib.modeling.nets import mobilenet
from lib.modeling.nets import darknet
networks_map = {
                    'vgg16': vgg.vgg16,
                    'vgg16_S1L2': vgg.vgg16_S1L2,
                    'vgg16_S2L2_5': vgg.vgg16_S2L2_5,
                    'resnet_18': resnet.resnet_18,
                    'resnet_34': resnet.resnet_34,
                    'resnet_50': resnet.resnet_50,
                    'resnet_101': resnet.resnet_101,
                    'mobilenet_v1': mobilenet.mobilenet_v1,
                    'mobilenet_v1_S1L6':mobilenet.mobilenet_v1_S1L6,
                    'mobilenet_v1_S2L0_6':mobilenet.mobilenet_v1_S2L0_6,
                    'mobilenet_v1_S1L4': mobilenet.mobilenet_v1_S1L4,
                    'mobilenet_v1_S1L0': mobilenet.mobilenet_v1_S1L0,
                    'mobilenet_v1_075': mobilenet.mobilenet_v1_075,
                    'mobilenet_v1_050': mobilenet.mobilenet_v1_050,
                    'mobilenet_v1_025': mobilenet.mobilenet_v1_025,
                    'mobilenet_v2': mobilenet.mobilenet_v2,
                    'mobilenet_v2_075': mobilenet.mobilenet_v2_075,
                    'mobilenet_v2_050': mobilenet.mobilenet_v2_050,
                    'mobilenet_v2_025': mobilenet.mobilenet_v2_025,
                    'darknet_19': darknet.darknet_19,
                    'darknet_53': darknet.darknet_53,
               }

from lib.layers.functions.prior_box import PriorBox
import torch

def _forward_features_size(model, img_size):
    model.eval()
    x = torch.rand(1, 3, img_size[0], img_size[1])
    x = torch.autograd.Variable(x, volatile=True) #.cuda()
    feature_maps = model(x, phase='feature')
    return [(o.size()[2], o.size()[3]) for o in feature_maps]


def create_model(cfg):
    '''
    '''
    #
    base = networks_map[cfg.NETS]
    number_box= [2*len(aspect_ratios) if isinstance(aspect_ratios[0], int) else len(aspect_ratios) for aspect_ratios in cfg.ASPECT_RATIOS]  
        
    model = ssds_map[cfg.SSDS](base=base, feature_layer=cfg.FEATURE_LAYER, mbox=number_box, num_classes=cfg.NUM_CLASSES)
    #
    feature_maps = _forward_features_size(model, cfg.IMAGE_SIZE)
    [print(str(k)+str(f)) for k,f in enumerate(model.base)]
    print('==>Feature map size:')
    print(feature_maps)
    # 
    priorbox = PriorBox(image_size=cfg.IMAGE_SIZE, feature_maps=feature_maps, aspect_ratios=cfg.ASPECT_RATIOS, 
                    scale=cfg.SIZES, archor_stride=cfg.STEPS, clip=cfg.CLIP)
    # priors = Variable(priorbox.forward(), volatile=True)

    return model, priorbox