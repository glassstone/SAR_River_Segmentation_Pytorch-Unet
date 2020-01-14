import torch
import torch.nn.functional as F
from tqdm import tqdm

from dice_loss import dice_coeff


def eval_net(net, loader, device, n_val):
    """Evaluation without the densecrf with the dice coefficient"""
    net.eval()
    tot = 0
    confMatrix = np.zeros((2,2))
    with tqdm(total=n_val, desc='Validation round', unit='img', leave=False) as pbar:
        for batch in loader:
            imgs = batch['image']
            true_masks = batch['mask']

            imgs = imgs.to(device=device, dtype=torch.float32)
            true_masks = true_masks.to(device=device, dtype=torch.float32)

            mask_pred = net(imgs)

            mask_pred = net(imgs)
            mask_pred = (mask_pred > 0.5).int()
            correct = (true_masks == mask_pred)
            tot += torch.sum(correct).item()
    return tot / (n_val * 572 * 572)

    #        for idx, true_mask in enumerate(true_masks):
    #            mask_pred = (mask_pred > 0.5).float()
    #            if net.n_classes > 1:
    #                tot += F.cross_entropy(mask_pred.unsqueeze(dim=0), true_mask.unsqueeze(dim=0)).item()
    #            else:
    #                tot += dice_coeff(mask_pred, true_mask.squeeze(dim=1)).item()
    #        pbar.update(imgs.shape[0])

    #return tot / n_val
